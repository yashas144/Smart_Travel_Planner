# main_app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

KNOWLEDGE_AGENT_URL = "http://127.0.0.1:5001/get_attractions"
FLIGHT_AGENT_URL = "http://127.0.0.1:5002/get_flight_options"

@app.route('/api/plan_trip', methods=['POST'])
def plan_trip_endpoint():
    user_request = request.get_json()
    city = user_request.get('city')
    origin = user_request.get('origin')
    travel_date = user_request.get('travel_date')

    if not all([city, origin, travel_date]):
        return jsonify({"error": "All fields are required!"}), 400

    try:
        # Call Knowledge Agent
        knowledge_payload = {"city": city}
        knowledge_response = requests.post(KNOWLEDGE_AGENT_URL, json=knowledge_payload)
        knowledge_response.raise_for_status()
        knowledge_data = knowledge_response.json()
        
        # Call Flight Agent
        # The flight agent expects the destination city to be an IATA code, like 'LAX'
        flight_payload = {"origin": origin, "destination": city, "date": travel_date}
        flight_response = requests.post(FLIGHT_AGENT_URL, json=flight_payload)
        flight_response.raise_for_status()
        flight_data = flight_response.json()

        # --- !! THIS IS THE FIX !! ---
        # The frontend expects data inside a "raw_data" object.
        # We also need to extract the list from the agent's response.
        final_plan = {
            "summary": f"Here is your AI-Generated trip plan for {city}, departing from {origin} on {travel_date}.",
            "raw_data": {
                "flights": flight_data.get('flights', []),  # Extract the list of flights
                "activities": knowledge_data.get('activities', [])  # Extract the list of activities
            },
            "metadata": {
                # This helps the frontend display service status
                "services_used": ["flight", "knowledge", "rag"]
            }
        }
        
        return jsonify(final_plan)

    except requests.exceptions.RequestException as e:
        error_message = "An AI agent is currently unavailable. Please try again later."
        # Check which agent failed
        if KNOWLEDGE_AGENT_URL in str(e):
            error_message = "The Knowledge Agent is unavailable."
        elif FLIGHT_AGENT_URL in str(e):
            error_message = "The Flight Agent is unavailable."
        
        return jsonify({"error": error_message, "details": str(e)}), 503

if __name__ == '__main__':
    app.run(port=5000)


























'''# main_app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

KNOWLEDGE_AGENT_URL = "http://127.0.0.1:5001/get_attractions"
# CORRECTED: Point this to the new multi-flight endpoint in the flight agent
FLIGHT_AGENT_URL = "http://127.0.0.1:5002/get_flight_options" # <-- CHANGED

@app.route('/api/plan_trip', methods=['POST'])
def plan_trip_endpoint():
    # ... (code for user_request and knowledge_agent call remains the same)
    user_request = request.get_json()
    city = user_request.get('city')
    origin = user_request.get('origin')
    travel_date = user_request.get('travel_date')

    if not all([city, origin, travel_date]):
        return jsonify({"error": "All fields are required!"}), 400

    try:
        knowledge_payload = {"city": city}
        knowledge_response = requests.post(KNOWLEDGE_AGENT_URL, json=knowledge_payload)
        knowledge_response.raise_for_status()
        knowledge_data = knowledge_response.json()
        
        # Call Flight Agent
        flight_payload = {"origin": origin, "destination": city, "date": travel_date}
        flight_response = requests.post(FLIGHT_AGENT_URL, json=flight_payload) #<-- This now calls the correct endpoint
        flight_response.raise_for_status()
        flight_data = flight_response.json()

        # Combine results
        final_plan = {
            "summary": f"Your trip to {city} from {origin}",
            "flight_details": flight_data, # flight_data now contains {"flights": [...]}
            "suggested_activities": knowledge_data.get('activities', [])
        }
        
        return jsonify(final_plan)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An AI agent is currently unavailable. Please try again later.", "details": str(e)}), 503

if __name__ == '__main__':
    app.run(port=5000)'''




























'''# main_app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Updated Agent URL
KNOWLEDGE_AGENT_URL = "http://127.0.0.1:5001/get_attractions" # <-- CHANGED
FLIGHT_AGENT_URL = "http://127.0.0.1:5002/get_flight_options" # <-- CHANGED

@app.route('/api/plan_trip', methods=['POST'])
def plan_trip_endpoint():
    user_request = request.get_json()
    city = user_request.get('city')
    origin = user_request.get('origin')
    travel_date = user_request.get('travel_date')

    if not all([city, origin, travel_date]):
        return jsonify({"error": "All fields are required!"}), 400

    try:
        # 1. Call the new Knowledge Agent
        knowledge_payload = {"city": city}
        knowledge_response = requests.post(KNOWLEDGE_AGENT_URL, json=knowledge_payload) # <-- CHANGED
        knowledge_response.raise_for_status()
        knowledge_data = knowledge_response.json()

        # 2. Call Flight Agent (no changes here)
        flight_payload = {"origin": origin, "destination": city, "date": travel_date}
        flight_response = requests.post(FLIGHT_AGENT_URL, json=flight_payload)
        flight_response.raise_for_status()
        flight_data = flight_response.json()

        # --- Combine results ---
        final_plan = {
            "summary": f"Your trip to {city} from {origin}",
            "flight_details": flight_data,
            "suggested_activities": knowledge_data.get('activities', [])
        }
        
        return jsonify(final_plan)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "An AI agent is currently unavailable. Please try again later.", "details": str(e)}), 503

if __name__ == '__main__':
    app.run(port=5000)'''