import stripe
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.extensions import db
from backend.models.payment import Payment
from backend.models.user import User
from datetime import datetime

payments_bp = Blueprint("payments", __name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PLANS = {
    "basic_1_month": {"amount": 100, "name": "Starter Plan", "duration": 30, "leads": 40},
    "pro_3_month": {"amount": 400, "name": "Growth Plan", "duration": 90, "leads": 100}
}


# -------------------------------------------------
# 💳 CREATE CHECKOUT SESSION (SECURE)
# -------------------------------------------------
@payments_bp.route("/create-checkout-session", methods=["POST"])
@jwt_required()
def create_checkout_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    plan = data.get("plan")

    if plan not in PLANS:
        return jsonify({"error": "Invalid plan"}), 400

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": PLANS[plan]["name"]},
                "unit_amount": PLANS[plan]["amount"],
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:3000/dashboard?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:3000/payment",
        metadata={
            "user_id": str(user_id),
            "plan": plan
        }
    )

    return jsonify({"url": checkout_session.url})


# -------------------------------------------------
# ✅ CONFIRM PAYMENT (VERIFY STRIPE SESSION)
# -------------------------------------------------
@payments_bp.route("/confirm", methods=["POST"])
@jwt_required()
def confirm_payment():
    user_id = get_jwt_identity()
    data = request.get_json()
    stripe_session_id = data.get("session_id")

    if not stripe_session_id:
        return jsonify({"error": "Session ID required"}), 400

    try:
        session = stripe.checkout.Session.retrieve(stripe_session_id)

        if session.payment_status != "paid":
            return jsonify({"error": "Payment not completed"}), 400

        plan = session.metadata.get("plan")

        if plan not in PLANS:
            return jsonify({"error": "Invalid plan metadata"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        payment = Payment(
            user_id=user_id,
            plan_name=plan,
            amount=PLANS[plan]["amount"] / 100,
            duration_days=PLANS[plan]["duration"],
            leads_per_day=PLANS[plan]["leads"]
        )

        payment.activate()
        db.session.add(payment)

        user.is_paid = True
        db.session.commit()

        return jsonify({"message": "Subscription activated"}), 200

    except Exception:
        return jsonify({"error": "Payment verification failed"}), 500
