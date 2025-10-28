import os
import json
import requests
from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# --- Global In-Memory Store for Load Balancing ---
REQUEST_COUNTS = {}

def get_models_from_env():
    """Parses environment variables to build the list of general models."""
    models = []
    i = 1
    while True:
        api_key = os.environ.get(f'API_KEY_{i}')
        model_name = os.environ.get(f'MODEL_NAME_{i}')
        if api_key and model_name:
            model_id = f'model_{i}'
            models.append({'id': model_id, 'apiKey': api_key, 'model': model_name})
            if model_id not in REQUEST_COUNTS:
                REQUEST_COUNTS[model_id] = 0
            i += 1
        else:
            break
    return models

def handle_ncert_query(user_query, referer):
    pdf_context = get_simulated_ncert_context(user_query)
    system_prompt = "You are a precise NCERT Tutor AI. Answer based ONLY on the provided textbook context. If the context is insufficient, state that clearly before providing a general answer. Format all responses in clean HTML."
    final_prompt = f"--- TEXTBOOK CONTEXT ---\n{pdf_context}\n--- END OF CONTEXT ---\n\nBased strictly on the context, answer: \"{user_query}\""
    
    api_key = os.environ.get('API_KEY_NCERT')
    model_name = os.environ.get('MODEL_NAME_NCERT', 'anthropic/claude-3-haiku')
    
    if not api_key:
        raise Exception("API_KEY_NCERT is not configured in the environment.")

    response_content = call_openrouter(api_key, model_name, system_prompt, final_prompt, referer)
    return {"reply": response_content, "modelName": "NCERT Tutor"}

def handle_general_query(messages, referer):
    general_models = get_models_from_env()
    if not general_models:
        raise Exception("No general API keys (API_KEY_1, etc.) are configured.")

    sorted_models = sorted(general_models, key=lambda m: REQUEST_COUNTS.get(m['id'], 0))
    selected_model = sorted_models[0]
    
    user_prompt = messages[-1]['content']
    system_prompt = messages[0]['content']
    
    response_content = call_openrouter(selected_model['apiKey'], selected_model['model'], system_prompt, user_prompt, referer)
    
    REQUEST_COUNTS[selected_model['id']] += 1
    
    return {"reply": response_content, "modelName": selected_model['model'].replace(':free', '')}

def call_openrouter(api_key, model, system_prompt, user_prompt, referer):
    headers = {"Authorization": f"Bearer {api_key}", "HTTP-Referer": referer or "", "X-Title": "Callanix-Backend"}
    payload = {"model": model, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]}
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=45)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_simulated_ncert_context(user_query):
    query_lower = user_query.lower()
    if all(k in query_lower for k in ["newton", "law", "9"]):
        return "From NCERT Class 9 Science, Chapter 9: Force and Laws of Motion: Newton's First Law states an object at rest stays at rest unless a force acts on it. The Second Law is F=ma. The Third Law states every action has an equal and opposite reaction."
    if all(k in query_lower for k in ["cell", "fundamental unit", "9"]):
        return "From NCERT Class 9 Science, Chapter 5: The Fundamental Unit of Life: The cell is the basic structural and functional unit of life. Robert Hooke discovered it. Prokaryotic cells lack a nucleus, while Eukaryotic cells have one."
    return "Could not find specific context in the simulated NCERT textbook content."

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            path = self.path
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            referer = self.headers.get('Referer')

            if path == '/api/ask-ncert':
                response_data = handle_ncert_query(data['query'], referer)
            elif path == '/api/ask-general':
                response_data = handle_general_query(data['messages'], referer)
            else:
                self._send_error("Endpoint not found.", 404)
                return
            self._send_response(response_data)
        except Exception as e:
            self._send_error(f"An internal error occurred: {str(e)}", 500)

    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _send_error(self, message, status_code=400):
        self._send_response({"error": message}, status_code)
        
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()