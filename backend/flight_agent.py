# flight_agent.py (Upgraded with Live API and Fallback)

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY") 
AVIATIONSTACK_API_URL = "http://api.aviationstack.com/v1/flights"

# --- Fallback data if API fails ---
MOCK_FLIGHT_DATA = {
    "flights": [{
        "airline": "Fallback Airlines",
        "flight_number": "FA-123",
        "departure_airport": "Origin Airport",
        "departure_time": "N/A",
        "arrival_airport": "Destination Airport",
        "arrival_time": "N/A",
        "status": "Service Unavailable",
        "price_usd": "N/A",
        "source": "mock" # To indicate this is not real data
    }]
}

@app.route('/get_flight_options', methods=['POST'])
def get_flight_options():
    data = request.get_json()
    origin_iata = data.get('origin')
    destination_iata = data.get('destination')

    if not all([origin_iata, destination_iata]):
        return jsonify({"error": "Origin and Destination IATA codes are required"}), 400

    if not AVIATIONSTACK_API_KEY:
        print("Flight Agent: AVIATIONSTACK_API_KEY not found. Returning mock data.")
        return jsonify(MOCK_FLIGHT_DATA)

    api_params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'dep_iata': origin_iata.upper(),
        'arr_iata': destination_iata.upper(),
        'limit': 3
    }

    try:
        api_response = requests.get(AVIATIONSTACK_API_URL, params=api_params, timeout=5)
        api_response.raise_for_status()
        response_data = api_response.json()
        
        flight_options = []
        for flight in response_data.get('data', []):
            option = {
                "airline": flight['airline']['name'],
                "flight_number": flight['flight']['iata'],
                "departure_airport": flight['departure']['airport'],
                "departure_time": flight['departure']['scheduled'],
                "arrival_airport": flight['arrival']['airport'],
                "arrival_time": flight['arrival']['scheduled'],
                "status": flight['flight_status'],
                "price_usd": "Contact airline for price"
            }
            flight_options.append(option)
            
        if not flight_options:
             return jsonify({"flights": [{"airline": "No direct flights found for this route.", "price_usd": "N/A"}]})

        return jsonify({"flights": flight_options})

    except requests.exceptions.RequestException as e:
        # --- !! THIS IS THE FIX !! ---
        # If the API call fails, return mock data instead of an error
        print(f"Flight Agent API call failed: {e}. Returning mock data.")
        return jsonify(MOCK_FLIGHT_DATA)

if __name__ == '__main__':
    app.run(port=5002)















'''# flight_agent.py (Upgraded with Live API)

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# --- IMPORTANT ---
# Paste the API key you got from AviationStack here
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY") 
#AVIATIONSTACK_API_KEY = "4deab6a9375f2a1b99f759575b9899cd"
AVIATIONSTACK_API_URL = "http://api.aviationstack.com/v1/flights"

@app.route('/get_flight_options', methods=['POST'])
def get_flight_options():
    """
    Fetches real flight options from the AviationStack API.
    Expects IATA codes for origin and destination.
    """
    data = request.get_json()
    origin_iata = data.get('origin')
    destination_iata = data.get('destination')

    if not all([origin_iata, destination_iata]):
        return jsonify({"error": "Origin and Destination IATA codes are required"}), 400

    api_params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'dep_iata': origin_iata.upper(),
        'arr_iata': destination_iata.upper(),
        'limit': 5 # Get up to 5 flight options
    }

    try:
        # Call the external AviationStack API
        api_response = requests.get(AVIATIONSTACK_API_URL, params=api_params)
        api_response.raise_for_status() # Raise an exception for bad status codes
        
        response_data = api_response.json()
        
        flight_options = []
        # The 'data' key holds the list of flights
        for flight in response_data.get('data', []):
            option = {
                "airline": flight['airline']['name'],
                "flight_number": flight['flight']['iata'],
                "departure_airport": flight['departure']['airport'],
                "departure_time": flight['departure']['scheduled'],
                "arrival_airport": flight['arrival']['airport'],
                "arrival_time": flight['arrival']['scheduled'],
                "status": flight['flight_status']
            }
            # Use a more descriptive price placeholder, as free plan doesn't include it
            option['price_usd'] = "Contact airline for price"
            flight_options.append(option)
            
        if not flight_options:
            return jsonify({"flights": [{"airline": "No flights found for this route.", "price_usd": "N/A"}]})

        return jsonify({"flights": flight_options})

    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return jsonify({"error": "Failed to connect to the flight data provider."}), 503
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # The API sometimes sends back errors in a different format
        error_details = api_response.json().get('error', {}).get('info', 'Unknown error')
        return jsonify({"error": "Error retrieving flight data.", "details": error_details}), 500


if __name__ == '__main__':
    app.run(port=5002)'''