import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables before initializing the client
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_personalized_email(lead):
    name = lead.name or "there"
    
    # Check if it's a B2C lead to customize the prompt
    if lead.lead_type == 'b2c':
        interests = lead.interests or "new trends"
        location = lead.location or "your area"
        prompt = (
            f"Write a 2-sentence friendly email to {name} in {location}. "
            f"Mention their interest in {interests} and offer a 20% discount "
            f"on SalesMind AI's consumer platform. Keep it casual and helpful."
        )
    else:
        # Standard B2B prompt
        company = lead.company or "your company"
        job_title = lead.job_title or "professional"
        prompt = (
            f"Write a short, professional 2-sentence sales email to {name} "
            f"at {company} as a {job_title}. Introduce SalesMind AI."
        )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hi {name}, we have an exclusive offer for you based on your interests!"