from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from backend.services.ai_service import client 
from backend.services.rag_service import retrieve_relevant_context
from backend.utils.security_utils import scan_for_prompt_injection, mask_pii

chat_bp = Blueprint("chat", __name__)

SYSTEM_PROMPT = """
You are the official SalesMind AI Support Bot. 
Your ONLY goal is to answer questions about SalesMind AI using the provided context.

RULES:
1. If the context contains the answer, be concise and helpful.
2. If the context does NOT contain the answer, or the user is asking about general topics, say: "I'm sorry, I am only trained to answer questions regarding SalesMind AI services."
3. Never mention that you are an AI or that you have 'context'. Just answer as the company representative.
"""

# The route is set to "" to match the blueprint prefix "/api/chat" exactly in Postman
@chat_bp.route("/", methods=["POST"]) 
@jwt_required()
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "I'm listening! Ask me anything about SalesMind."}), 400

    # 1. Security: Check for Prompt Injection
    if scan_for_prompt_injection(user_message):
        return jsonify({
            "reply": "I'm sorry, I cannot process this request due to safety bypass attempts."
        }), 400

    # 2. Privacy: Mask PII
    safe_user_message = mask_pii(user_message)

    # DEBUG: Moved above RAG check so masking is always visible in the terminal
    print(f"\n--- DEBUG: Message sent to Groq: {safe_user_message} ---\n")

    # 3. Retrieval: Get context from RAG
    context = retrieve_relevant_context(user_message)

    # 4. Guardrail: Refuse if no context found
    if not context:
        return jsonify({"reply": "I'm sorry, I am only trained to answer questions regarding SalesMind AI services."})
    
    try:
        # Using a stable Groq model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context: {context}\n\nUser Question: {safe_user_message}"}
            ],
            temperature=0.1
        )
        return jsonify({"reply": response.choices[0].message.content})
    
    except Exception as e:
        # Error will be visible in the terminal
        print(f"Chatbot Error: {e}") 
        return jsonify({"reply": "I'm having trouble connecting to my brain. Try again?"}), 500