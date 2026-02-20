from flask import Blueprint, Response, request, jsonify
import pandas as pd
import io
import uuid
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.lead import Lead
from backend.models.user import User
from backend.extensions import db
from backend.utils.tasks import fetch_leads_task
from backend.utils.security_utils import is_file_secure 

leads_bp = Blueprint("leads", __name__)

REQUIRED_COLUMNS = {"name", "email", "company", "job_title"}
MAX_ROWS = 500
MAX_TRIAL_ROUNDS = 3

def sanitize_csv_value(value):
    val_str = str(value).strip()
    if val_str.startswith(("=", "+", "-", "@")):
        return "'" + val_str
    return val_str

@leads_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_leads():
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # 1. Extension Check
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files allowed"}), 400
    
    # 2. Deep Check: Magic Bytes & Binary detection
    is_secure, error_msg = is_file_secure(file)
    if not is_secure:
        return jsonify({"message": error_msg}), 400

    try:
        file.seek(0)
        content = file.read().decode("utf-8")
        
        # 1. NEW: tell pandas to RAISE an error if a line has the wrong number of commas
        df = pd.read_csv(io.StringIO(content), on_bad_lines='error')

        if len(df) == 0:
            return jsonify({"error": "CSV file is empty"}), 400

        if len(df) > MAX_ROWS:
            return jsonify({"error": f"Max {MAX_ROWS} rows allowed"}), 400

        df.columns = [c.lower().strip() for c in df.columns]

        if not REQUIRED_COLUMNS.issubset(df.columns):
            return jsonify({"error": f"Missing required columns: {REQUIRED_COLUMNS}"}), 400

        added = 0
        for _, row in df.iterrows():
            # 1. ENHANCED: Strict Validation Check
            # We check for NaN, None, or just empty white-space strings
            name = str(row.get('name', '')).strip()
            email = str(row.get('email', '')).strip()
            company = str(row.get('company', '')).strip()

            if not name or not email or not company or name.lower() == 'nan':
                return jsonify({"error": "Invalid CSV format: Missing data in required rows"}), 400

            
            # 2. Process the raw email first (clean and lowercase)
            raw_email = str(row["email"]).strip().lower()

            # 3. Check for duplicates using the clean email
            if Lead.query.filter_by(email=raw_email, user_id=user_id).first():
                continue

            # 4. Apply sanitization to ALL fields at the moment of assignment
            lead = Lead(
                name=sanitize_csv_value(row["name"]),
                email=sanitize_csv_value(raw_email), # Sanitize the already-lowercased email
                company=sanitize_csv_value(row["company"]),
                job_title=sanitize_csv_value(row["job_title"]),
                user_id=user_id,
                source="CSV_UPLOAD",
                session_id=str(uuid.uuid4())
            )
            db.session.add(lead)
            added += 1

        db.session.commit()
        return jsonify({"message": f"{added} leads imported"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Invalid CSV format"}), 400

@leads_bp.route("/generate_on_demand", methods=["POST"])
@jwt_required()
def generate_on_demand():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or "industry" not in data:
        return jsonify({"error": "Industry required"}), 400

    industry = data["industry"]
    session_id = str(uuid.uuid4())
    user = User.query.get(user_id)

    if not user.is_paid and user.trial_rounds_used >= MAX_TRIAL_ROUNDS:
        return jsonify({"error": "Trial limit exceeded", "require_payment": True}), 403

    task = fetch_leads_task.delay(industry, session_id, user_id)
    if not user.is_paid:
        user.trial_rounds_used += 1
        db.session.commit()

    return jsonify({"message": "Lead generation started", "task_id": task.id, "session_id": session_id}), 202

@leads_bp.route("/by-session", methods=["GET"])
@jwt_required()
def get_leads_by_session():
    user_id = get_jwt_identity()
    session_id = request.args.get("session_id")
    leads = Lead.query.filter_by(session_id=session_id, user_id=user_id).all()
    return jsonify([l.to_dict() for l in leads]), 200

@leads_bp.route("/download", methods=["GET"])
@jwt_required()
def download_leads():
    user_id = get_jwt_identity()
    session_id = request.args.get("session_id")
    leads = Lead.query.filter_by(session_id=session_id, user_id=user_id).all()
    
    df = pd.DataFrame([{
        "name": l.name, "email": l.email, "company": l.company, "job_title": l.job_title
    } for l in leads])

    return Response(df.to_csv(index=False), mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename=leads_{session_id}.csv"})

@leads_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_lead_stats():
    user_id = get_jwt_identity()
    total = Lead.query.filter_by(user_id=user_id).count()
    return {"total_leads": total}, 200