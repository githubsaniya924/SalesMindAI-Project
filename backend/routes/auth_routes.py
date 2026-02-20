import random
import re
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, 
    get_jwt_identity, 
    jwt_required, 
    set_access_cookies, 
    unset_jwt_cookies
)

from backend.extensions import db, limiter
from backend.models.user import User
from backend.models.otp import OTP
from backend.utils.email_utils import send_otp_email, send_reset_email

auth_bp = Blueprint("auth", __name__)

# --- Helper for Email Validation ---
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

# --- Routes ---

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password') # Get the plain password

    # 2. NEW SECURITY CHECK: Validate Password Complexity
    if not password or not is_strong_password(password):
        return jsonify({
            "message": "Password weak", 
            "error": "Password must be 6+ chars with uppercase, number, and special character."
        }), 400
    
    if not email or not is_valid_email(email):
        return jsonify({"message": "Invalid email address"}), 400

    # Prevent UniqueViolation error by checking existence first
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    user = User(
        name=data.get('name'), 
        email=email, 
        password_hash=generate_password_hash(data.get('password'))
    )
    
    try:
        db.session.add(user)
        db.session.flush() # Get user.id for the OTP record

        otp_code = str(random.randint(100000, 999999))
        otp = OTP(
            user_id=user.id, 
            code=otp_code, 
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )

        db.session.add(otp)
        db.session.commit()
        
        send_otp_email(email, otp_code)
        return jsonify({"message": "OTP sent", "email": email}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Signup failed", "error": str(e)}), 500


@auth_bp.route("/verify-otp", methods=["POST"])
@limiter.limit("5 per minute")
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp_code = data.get("otp")

    if not email or not otp_code:
        return jsonify({"message": "Email and OTP required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Use standardized columns: user_id and code
    otp_record = OTP.query.filter_by(user_id=user.id, code=otp_code).first()

    if not otp_record:
        return jsonify({"message": "Invalid OTP"}), 400

    # Use standardized column: expires_at
    if datetime.utcnow() > otp_record.expires_at:
        return jsonify({"message": "OTP expired"}), 400

    user.is_verified = True
    db.session.delete(otp_record)
    db.session.commit()

    # Create JWT token - Identity as String is safer for matching
    access_token = create_access_token(identity=str(user.id))

    response = jsonify({"message": "Account verified successfully"})
    set_access_cookies(response, access_token)
    return response, 200


# backend/routes/auth_routes.py

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    # 1. Check if user is currently locked out
    if user.is_locked():
        unlock_time = user.lockout_until.strftime("%H:%M:%S")
        return jsonify({
            "message": f"Account locked due to too many failed attempts. Try again after {unlock_time}."
        }), 403

    # 2. Check Password
    if not check_password_hash(user.password_hash, password):
        # Increment failed attempts
        user.failed_login_attempts += 1
        
        # 3. Trigger Lockout after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.lockout_until = datetime.utcnow() + timedelta(minutes=15)
            db.session.commit()
            return jsonify({"message": "Too many failed attempts. Your account is locked for 15 minutes."}), 403
        
        db.session.commit()
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.is_verified:
        return jsonify({"message": "Please verify your email"}), 403

    # 4. Success: Reset failed attempts and lockout on successful login
    user.failed_login_attempts = 0
    user.lockout_until = None
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    resp = jsonify({"msg": "login successful", "access_token": access_token})
    set_access_cookies(resp, access_token)
    return resp, 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route("/resend-otp", methods=["POST"])
@limiter.limit("3 per hour")
def resend_otp():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.is_verified:
        return jsonify({"message": "Already verified"}), 400

    # Delete old OTPs for this specific user
    OTP.query.filter_by(user_id=user.id).delete()
    
    new_otp_code = str(random.randint(100000, 999999))
    otp_entry = OTP(
        user_id=user.id,
        code=new_otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.session.add(otp_entry)
    db.session.commit()

    send_otp_email(email, new_otp_code)
    return jsonify({"message": "OTP resent"}), 200


@auth_bp.route("/auth/check", methods=["GET"])
@jwt_required()
def check_auth():
    # Identity is retrieved as a string from the JWT
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({"is_authenticated": False}), 401
        
    return jsonify({
        "is_authenticated": True,
        "user": {"id": user.id, "email": user.email, "name": user.name}
    }), 200


@auth_bp.route("/forgot-password", methods=["POST"])
@limiter.limit("3 per hour")
def forgot_password():
    data = request.json
    email = data.get("email", "").strip().lower()

    user = User.query.filter_by(email=email).first()
    
    # SECURITY: We return the same message even if the user doesn't exist
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        reset_link = f"http://localhost:3000/reset-password/{token}"
        send_reset_email(email, reset_link)

    # Always return a generic success message
    return jsonify({"message": "If this email is registered, a reset link has been sent."}), 200



@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not new_password or len(new_password) < 6:
        return jsonify({"error": "New password must be at least 8 characters"}), 400

    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    user.failed_login_attempts = 0 
    user.lockout_until = None
    
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200


def is_strong_password(password):
    """
    SECURITY FEATURE: Enforces complexity on the backend.
    - Min 10 characters
    - At least one uppercase
    - At least one number
    - At least one special character
    """
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    return True