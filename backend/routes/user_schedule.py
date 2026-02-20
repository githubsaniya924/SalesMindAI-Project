# backend/routes/user_schedule.py
from flask import Blueprint, request, jsonify
from backend.extensions import db
from backend.models.schedule import UserSchedule 
import json # Used to handle criteria_json

schedule_bp = Blueprint("schedule", __name__)

@schedule_bp.route("/set_schedule", methods=["POST"])
def set_lead_schedule():
    data = request.json
    user_id = data.get('user_id') # Assume user ID is passed or derived from session
    
    # 1. Capture the criteria for the daily 9 AM run
    criteria = {
        'domain': data.get('domain'),
        'location': data.get('location'),
        'title_keyword': data.get('title_keyword')
    }
    
    # 2. Hardcode 9 AM as the scheduled time
    scheduled_time = "09:00" 

    # 3. Save or update the schedule in the database
    schedule = UserSchedule.query.filter_by(user_id=user_id).first()
    if not schedule:
        schedule = UserSchedule(user_id=user_id, scheduled_time=scheduled_time)
        db.session.add(schedule)
        
    schedule.criteria_json = criteria
    db.session.commit()
    
    return jsonify({"message": f"Daily lead generation set for {scheduled_time} with new criteria."}), 200

# Remember to register schedule_bp in app.py    