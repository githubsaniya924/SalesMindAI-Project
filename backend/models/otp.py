from datetime import datetime, timedelta
from backend.extensions import db

class OTP(db.Model):
    __tablename__ = "otps"

    id = db.Column(db.Integer, primary_key=True)

    # ✅ Link OTP to user
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # ✅ OTP code
    code = db.Column(db.String(6), nullable=False)

    # ✅ Expiry
    expires_at = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at
