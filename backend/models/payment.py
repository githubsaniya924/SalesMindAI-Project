from backend.extensions import db
from datetime import datetime, timedelta
from backend.models.user import User  

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    plan_name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    leads_per_day = db.Column(db.Integer, default=40)
    duration_days = db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(User, backref="payments")  # ✅ class, not string

    def activate(self):
        self.start_date = datetime.utcnow()
        self.end_date = self.start_date + timedelta(days=self.duration_days)
        self.is_active = True
