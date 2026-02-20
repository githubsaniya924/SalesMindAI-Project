# backend/models/schedule.py
from backend.extensions import db
from datetime import datetime

class UserSchedule(db.Model):
    __tablename__ = 'user_schedules'

    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key link to your User model (assuming your User model is named 'users')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False) 
    
    # Store the daily scheduled time (e.g., "09:00")
    scheduled_time = db.Column(db.String(5), nullable=False, default="09:00") 
    
    # Store the lead search criteria as JSON/dictionary 
    criteria_json = db.Column(db.JSON, nullable=False, default={})
    
    # Tracks the last successful run to prevent daily job duplication
    last_run_date = db.Column(db.Date) 

    # Optional relationship to the User model
    user = db.relationship('User', backref='schedule', uselist=False)

    def __repr__(self):
        return f"<UserSchedule UserID:{self.user_id} Time:{self.scheduled_time}>"