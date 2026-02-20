from backend.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # ✅ Email MUST be unique
    email = db.Column(db.String(150), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="sales_rep")

    # ✅ Verification flag
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trial_rounds_used = db.Column(db.Integer, default=0)
    is_paid = db.Column(db.Boolean, default=False)

    # Password Reset
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    # Security
    failed_login_attempts = db.Column(db.Integer, default=0)
    lockout_until = db.Column(db.DateTime, nullable=True)

    # ✅ Relationship with OTP
    otps = db.relationship(
        "OTP",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def has_active_plan(self):
        for payment in self.payments:
            if payment.is_active and payment.end_date > datetime.utcnow():
                return True
        return False

    def is_locked(self):
        return self.lockout_until and self.lockout_until > datetime.utcnow()

    def __repr__(self):
        return f"<User {self.email}>"


    