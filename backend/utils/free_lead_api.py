{"id":"58301","variant":"standard"}
import os
import requests
from sqlalchemy.exc import ProgrammingError

from flask import Blueprint, request, jsonify

from backend.models.lead import Lead
from backend.extensions import db

# --- CONFIG ---
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

# Blueprint
leads_bp = Blueprint("leads", __name__)

# --- Industry → Top Companies Mapping ---
INDUSTRY_COMPANIES = {
    "software": ["google.com", "microsoft.com", "zoom.us"],
    "finance": ["stripe.com", "paypal.com", "squareup.com"],
    "retail": ["amazon.com", "walmart.com", "target.com"],
    "healthcare": ["pfizer.com", "mckesson.com", "cvshealth.com"],
    "education": ["coursera.org", "udemy.com", "byjus.com"]
}


def fetch_emails_from_domain(domain):
    """Fetch emails using Hunter.io Domain Search."""
    url = f"https://api.hunter.io/v2/domain-search"

    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        emails = data.get("data", {}).get("emails", [])
        leads = []

        for e in emails:
            leads.append({
                "email": e.get("value"),
                "position": e.get("position"),
                "department": e.get("department"),
                "linkedin_url": e.get("linkedin"),
            })

        return leads

    except Exception as e:
        print(f"Error fetching Hunter.io emails for {domain}: {e}")
        return []


@leads_bp.route("/generate_on_demand", methods=["POST"])
def generate_on_demand():
    """Generate leads based on industry using Hunter.io"""
    data = request.get_json()
    industry = data.get("industry")

    if not industry:
        return jsonify({"error": "Industry is required"}), 400

    if industry not in INDUSTRY_COMPANIES:
        return jsonify({"error": "Industry not supported"}), 400

    domains = INDUSTRY_COMPANIES[industry]
    total_saved = 0

    for domain in domains:
        leads = fetch_emails_from_domain(domain)

        for l in leads:
            lead_data = {
                "name": None,
                "email": l.get("email"),
                "company": domain,
                "job_title": l.get("position"),
                "linkedin_url": l.get("linkedin_url"),
                "phone": None,
                "location": None,
                "industry": industry,
                "status": "new",
                "score": 0,
                "source": "Hunter.io",
                "apollo_id": None
            }

            try:
                Lead.create(**lead_data)
                total_saved += 1
            except ProgrammingError as e:
                print(f"Database Error: {e}")
                db.session.rollback()
            except Exception as e:
                print(f"Error savinga lead: {e}")
                db.session.rollback()

    return jsonify({
        "message": "Lead generation completed",
        "industry": industry,
        "total_saved": total_saved
    }), 200
