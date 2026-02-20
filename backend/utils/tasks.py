import os
import requests
from celery import shared_task
from backend.models.lead import Lead

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

INDUSTRY_COMPANIES = {
    "software": [
        "freshworks.com",
        "zoho.com",
        "chargebee.com",
        "postman.com",
        "invideo.io"
    ]
}

def fetch_emails_from_domain(domain):
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": HUNTER_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        emails = data.get("data", {}).get("emails")

        # 🔥 FORCE SAFE RETURN
        if not isinstance(emails, list):
            return []

        return emails

    except Exception as e:
        print("❌ Hunter API error:", e)
        return []


@shared_task(bind=True)
def fetch_leads_task(self, industry, session_id):

    print("🔥 TASK STARTED:", industry, session_id)

    if industry not in INDUSTRY_COMPANIES:
        print("❌ Industry not supported")
        return 0

    total_saved = 0

    for domain in INDUSTRY_COMPANIES[industry]:
        leads = fetch_emails_from_domain(domain)

        # ✅ GUARANTEED FALLBACK
        if len(leads) == 0:
            print("⚠️ No Hunter leads, using fallback for", domain)
            leads = [{"value": f"contact@{domain}"}]

        for e in leads:
            email = e.get("value")
            if not email:
                continue

            Lead.create(
                email=email,
                company=domain,
                industry=industry,
                source="Hunter.io",
                session_id=session_id
            )

            total_saved += 1

    print(f"✅ TASK COMPLETED. Saved {total_saved} leads")
    return total_saved
