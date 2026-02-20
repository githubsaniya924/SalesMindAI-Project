from backend.extensions import db 
from sqlalchemy.dialects.postgresql import JSONB

class LeadEnrichment(db.Model):
    __tablename__ = "lead_enrichments"

    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id", ondelete="CASCADE"))
    field_name = db.Column(db.String)
    field_value = db.Column(JSONB)
    enriched_at = db.Column(db.DateTime, server_default=db.func.now())
