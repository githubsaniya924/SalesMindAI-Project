# backend/models/lead.py

# Import db from extensions instead of app.py/init.py
from backend.extensions import db 
from sqlalchemy.dialects.postgresql import JSONB
from backend.models.user import User

class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    company = db.Column(db.String)
    job_title = db.Column(db.String)
    linkedin_url = db.Column(db.String)
    phone = db.Column(db.String)
    location = db.Column(db.String)
    industry = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String, default="new")
    score = db.Column(db.Integer, default=0)
    source = db.Column(db.String)
    # backend/models/lead.py
    user_id = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=True
)
    session_id = db.Column(db.String, index=True, nullable=True)


  

    user = db.relationship("User", backref="leads")

    # --- ADD THIS NEW COLUMN ---
    # Used to check for duplicates from the Apollo API source
    apollo_id = db.Column(db.String, unique=True, nullable=True) 
    

    # --- ADD THESE CLASS METHODS ---

    @classmethod
    def find_by_email_or_apollo_id(cls, email: str, apollo_id: str):
        """Finds a lead by email or Apollo ID to prevent duplicates."""
        # Use .first() to return the object or None
        return cls.query.filter(
            (cls.email == email) | (cls.apollo_id == apollo_id)
        ).first()

    @classmethod
    def create(cls, **kwargs):
        try:
            new_lead = cls(
                name=kwargs.get("name"),
                email=kwargs.get("email"),
                phone=kwargs.get("phone"),
                job_title=kwargs.get("job_title"),
                company=kwargs.get("company"),
                industry=kwargs.get("industry"),
                apollo_id=kwargs.get("apollo_id"),
                source=kwargs.get("source"),
                user_id=kwargs.get("user_id"),
                session_id=kwargs.get("session_id") 
            )
            db.session.add(new_lead)
            db.session.commit()
            return new_lead
        except Exception as e:
            db.session.rollback()
        raise e
