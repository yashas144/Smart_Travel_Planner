# knowledge_agent.py (UPDATED with RAG and Gemini API)

from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# --- Fallback data if API fails ---
FALLBACK_ACTIVITIES = {
    "activities": [
        "Explore local parks and green spaces.",
        "Visit a museum or historical site.",
        "Try the local cuisine at a highly-rated restaurant.",
        "Visit a popular shopping district or local market."
    ],
    "source": "fallback_due_to_api_error"
}

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Gemini Flash model
    GENERATION_MODEL = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Could not configure Gemini API: {e}")
    GENERATION_MODEL = None


# --- Simplified In-Memory Knowledge Base for RAG ---
KNOWLEDGE_BASE = [
    "Paris is famous for the Eiffel Tower, the Louvre Museum, Notre-Dame Cathedral, and the Arc de Triomphe. It's also known for its romantic ambiance and delicious pastries.",
    "New York City boasts iconic landmarks like Times Square, the Statue of Liberty, Central Park, the Empire State Building, and Broadway shows. It's a bustling metropolitan hub.",
    "Tokyo offers a unique blend of traditional temples (like Senso-ji) and futuristic skyscrapers (like Tokyo Skytree). Popular spots include Shibuya Crossing, Imperial Palace, and countless vibrant districts.",
]

@app.route('/get_attractions', methods=['POST'])
def get_attractions():
    data = request.get_json()
    city = data.get('city')

    if not city:
        return jsonify({"error": "City is a required field"}), 400

    # Fallback if Gemini model failed to initialize
    if not GENERATION_MODEL:
        print("Knowledge Agent: Gemini model not available, returning fallback data.")
        return jsonify(FALLBACK_ACTIVITIES)

    try:
        # --- RAG Pattern Implementation ---
        relevant_docs = [doc for doc in KNOWLEDGE_BASE if city.lower() in doc.lower()]
        context = "\n".join(relevant_docs) if relevant_docs else "No specific detailed information found in the knowledge base."

        prompt = f"""
        Based on the following information, suggest 3-5 top tourist attractions for {city}.
        --- Retrieved Information ---
        {context}
        --- End of Information ---
        Suggest activities for {city}:
        """

        print(f"Knowledge Agent: Sending prompt to Gemini for {city}...")
        response = GENERATION_MODEL.generate_content(prompt)
        
        generated_text = response.text.strip()
        attractions = [
            item.strip().replace('* ', '').replace('- ', '')
            for item in generated_text.split('\n')
            if item.strip()
        ]
        
        return jsonify({"activities": attractions[:5]})

    except Exception as e:
        # --- !! THIS IS THE FIX !! ---
        # If the API call fails (e.g., quota exceeded), return the fallback data
        print(f"Error in Knowledge Agent during Gemini call: {e}")
        print("Knowledge Agent: Returning fallback activities.")
        return jsonify(FALLBACK_ACTIVITIES)

if __name__ == '__main__':
    app.run(port=5001)
















'''# knowledge_agent.py (UPDATED with RAG and Gemini API)

from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
genai.configure(api_key=GEMINI_API_KEY)

for m in genai.list_models():
    print(f"Name: {m.name}, Supported Methods: {m.supported_generation_methods}")


# Initialize the Gemini Pro model for generation and embedding model
GENERATION_MODEL = genai.GenerativeModel('gemini-1.5-pro-latest')
EMBEDDING_MODEL = "models/embedding-001" # Gemini's embedding model

# --- Simplified In-Memory Knowledge Base for RAG ---
# In a real RAG system, this would be a vector database with actual document embeddings.
# For demonstration, we'll use a simple list of strings.
# We'll rely on the LLM's ability to find relevant info from these strings.
KNOWLEDGE_BASE = [
    "Paris is famous for the Eiffel Tower, the Louvre Museum, Notre-Dame Cathedral, and the Arc de Triomphe. It's also known for its romantic ambiance and delicious pastries.",
    "New York City boasts iconic landmarks like Times Square, the Statue of Liberty, Central Park, the Empire State Building, and Broadway shows. It's a bustling metropolitan hub.",
    "Tokyo offers a unique blend of traditional temples (like Senso-ji) and futuristic skyscrapers (like Tokyo Skytree). Popular spots include Shibuya Crossing, Imperial Palace, and countless vibrant districts.",
    "Rome is rich in history with the Colosseum, Roman Forum, Pantheon, and Vatican City. Don't forget the Trevi Fountain and delicious Italian cuisine.",
    "London features the Tower of London, Buckingham Palace, the British Museum, and Westminster Abbey. Enjoy a ride on the London Eye or explore its diverse neighborhoods.",
    "Dubai is known for its modern architecture, luxury shopping, and vibrant nightlife. Key attractions include the Burj Khalifa, The Dubai Mall, and the Palm Jumeirah."
    "Singapore is famous for its Gardens by the Bay, Marina Bay Sands, Sentosa Island, and vibrant hawker centers offering diverse food experiences.",
    "Sydney, Australia, is home to the Sydney Opera House, Sydney Harbour Bridge, Bondi Beach, and Taronga Zoo. It offers beautiful coastal views."
]

@app.route('/get_attractions', methods=['POST'])
def get_attractions():
    data = request.get_json()
    city = data.get('city')

    if not city:
        return jsonify({"error": "City is a required field"}), 400

    try:
        # --- RAG Pattern Implementation ---
        # 1. Query the "knowledge base" (simplified retrieval)
        # In a real scenario, you'd embed the city query and do a vector similarity search.
        # For this simplified example, we'll just consider any document that mentions the city.
        
        # This is a highly simplified 'retrieval' - a real RAG would use embeddings
        # to find semantic similarity. We're relying on the LLM to identify relevant docs.
        relevant_docs = [doc for doc in KNOWLEDGE_BASE if city.lower() in doc.lower()]

        context = "\n".join(relevant_docs) if relevant_docs else "No specific detailed information found in the knowledge base."

        # 2. Formulate a prompt with the retrieved context
        prompt = f"""
        You are an expert travel guide. Based on the following information, suggest 3-5 top tourist attractions or activities for {city}.
        If the information does not explicitly list attractions for {city}, use your general knowledge to suggest popular activities in a well-known city, or state that specific details for {city} are not available and offer general suggestions.

        --- Retrieved Information for {city} ---
        {context}
        --- End of Retrieved Information ---

        Suggest activities for {city}:
        """

        # 3. Use Gemini LLM to generate the answer based on context
        print(f"Knowledge Agent: Sending prompt to Gemini for {city}...")
        response = GENERATION_MODEL.generate_content(prompt)
        
        # Extract activities from the generated text
        # This part might need refinement based on Gemini's output format.
        # We expect it to list items, so we'll try to split by lines or common list markers.
        generated_text = response.text.strip()
        
        # Simple parsing: assume attractions are listed on separate lines or with bullet points
        attractions = [
            item.strip().replace('* ', '').replace('- ', '')
            for item in generated_text.split('\n')
            if item.strip()
        ]
        
        # Filter out generic phrases if the LLM couldn't find specific attractions
        if "no specific detailed information" in context.lower() or "not available" in generated_text.lower():
             return jsonify({"activities": [f"I couldn't find specific attractions for {city} in my detailed knowledge base, but generally you can explore local markets, historical sites, and enjoy the cuisine in such a city."]})
        
        return jsonify({"activities": attractions[:5]}) # Return top 5 if more are generated

    except Exception as e:
        print(f"Error in Knowledge Agent: {e}")
        return jsonify({"error": f"Failed to get attractions from knowledge base: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5001)'''