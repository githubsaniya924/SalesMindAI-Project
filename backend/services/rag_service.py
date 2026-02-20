from sentence_transformers import SentenceTransformer, util
import torch

# Load a slightly better model (still free/local)
model = SentenceTransformer("all-MiniLM-L6-v2")

KNOWLEDGE_BASE = [
    {"text": "SalesMind AI is an AI-powered sales automation platform.", "topic": "general"},
    {"text": "We provide B2B and B2C lead generation and email personalization.", "topic": "services"},
    {"text": "You can generate leads by connecting your email and setting your target criteria in the dashboard.", "topic": "leads"},
    {"text": "Pricing: Free ($0), Pro ($49/mo), and Enterprise ($199/mo).", "topic": "pricing"}
]

# Pre-embed the knowledge base
kb_texts = [item['text'] for item in KNOWLEDGE_BASE]
kb_embeddings = model.encode(kb_texts, convert_to_tensor=True)

def retrieve_relevant_context(query, threshold=0.35):
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    # Using Cosine Similarity via util for better accuracy
    cos_scores = util.cos_sim(query_embedding, kb_embeddings)[0]
    best_score_idx = torch.argmax(cos_scores).item()
    
    if cos_scores[best_score_idx] < threshold:
        return None

    return kb_texts[best_score_idx]