import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({ 
    city: '', 
    origin: '', 
    travel_date: '' 
  });
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState({
    main: false,
    flights: false,
    attractions: false,
    rag: false
  });
  const [error, setError] = useState('');
  const [serviceStatus, setServiceStatus] = useState({});

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading({
      main: true,
      flights: false,
      attractions: false,
      rag: false
    });
    setError('');
    setPlan(null);
    setServiceStatus({});

    try {
      const response = await fetch('http://127.0.0.1:5000/api/plan_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to plan trip');
      }

      setPlan(data);
      if (data.metadata?.services_used) {
        const status = {};
        data.metadata.services_used.forEach(service => {
          status[service] = 'operational';
        });
        if (!data.metadata.services_used.includes('knowledge')) {
          status.knowledge = 'unavailable';
        }
        if (!data.metadata.services_used.includes('flight')) {
          status.flight = 'unavailable';
        }
        if (!data.metadata.services_used.includes('rag')) {
          status.rag = 'unavailable';
        }
        setServiceStatus(status);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading({ main: false, flights: false, attractions: false, rag: false });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'operational': return 'green';
      case 'unavailable': return 'orange';
      default: return 'gray';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Travel Planner</h1>
        <p>AI-powered trip planning with RAG</p>
        <p className="author-name">Created by yashas chandra bathini</p>
      </header>
      
      <main>
        <form onSubmit={handleSubmit} className="trip-form">
          <input
            name="city"
            placeholder="Destination (e.g., Paris)"
            value={formData.city}
            onChange={handleInputChange}
            required
          />
          <input
            name="origin"
            placeholder="Origin Airport (e.g., JFK)"
            value={formData.origin}
            onChange={handleInputChange}
            required
          />
          <input
            name="travel_date"
            type="date"
            value={formData.travel_date}
            onChange={handleInputChange}
            required
          />
          <button type="submit" disabled={loading.main}>
            {loading.main ? 'Planning...' : 'Generate Trip Plan'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {Object.keys(serviceStatus).length > 0 && (
          <div className="service-status">
            <h3>Service Status:</h3>
            {Object.entries(serviceStatus).map(([service, status]) => (
              <p key={service}>
                {service}: <span style={{ color: getStatusColor(status) }}>
                  {status}
                </span>
              </p>
            ))}
          </div>
        )}

        {plan && (
          <div className="results">
            <div className="card summary-card">
              <h2>Your AI-Generated Trip Plan</h2>
              <div className="summary-content" style={{ whiteSpace: 'pre-line' }}>
                {plan.summary || "No summary available"}
              </div>
            </div>

            <div className="details-section">
              <div className="card">
                <h3>✈️ Flight Details</h3>
                {plan.raw_data?.flights?.length > 0 ? (
                  plan.raw_data.flights.map((flight, i) => (
                    <div key={i} className="flight-option">
                      <p><strong>{flight.airline} {flight.flight_number}</strong></p>
                      <p>{flight.departure_airport} → {flight.arrival_airport}</p>
                      <p>Departs: {flight.departure_time}</p>
                      <p>Arrives: {flight.arrival_time}</p>
                      <p>Status: {flight.status}</p>
                      {flight.source === 'mock' && <p className="mock-notice">Mock data</p>}
                    </div>
                  ))
                ) : (
                  <p>No flight information available</p>
                )}
              </div>

              <div className="card">
                <h3>🏛️ Recommended Activities</h3>
                {plan.raw_data?.activities?.length > 0 ? (
                  <ul>
                    {plan.raw_data.activities.map((activity, i) => (
                      <li key={i}>{activity}</li>
                    ))}
                  </ul>
                ) : (
                  <p>No activity suggestions available</p>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;























/* import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({ 
    city: '', 
    origin: '', 
    travel_date: '' 
  });
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState({
    main: false,
    flights: false,
    attractions: false,
    rag: false
  });
  const [error, setError] = useState('');
  const [serviceStatus, setServiceStatus] = useState({});

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading({
      main: true,
      flights: false,
      attractions: false,
      rag: false
    });
    setError('');
    setPlan(null);
    setServiceStatus({});

    try {
      const response = await fetch('http://127.0.0.1:5000/api/plan_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to plan trip');
      }

      setPlan(data);
      if (data.metadata?.services_used) {
        const status = {};
        data.metadata.services_used.forEach(service => {
          status[service] = 'operational';
        });
        if (!data.metadata.services_used.includes('knowledge')) {
          status.knowledge = 'unavailable';
        }
        if (!data.metadata.services_used.includes('flight')) {
          status.flight = 'unavailable';
        }
        if (!data.metadata.services_used.includes('rag')) {
          status.rag = 'unavailable';
        }
        setServiceStatus(status);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading({ main: false, flights: false, attractions: false, rag: false });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'operational': return 'green';
      case 'unavailable': return 'orange';
      default: return 'gray';
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Travel Planner</h1>
        <p>AI-powered trip planning with RAG</p>
      </header>
      
      <main>
        <form onSubmit={handleSubmit} className="trip-form">
          <input
            name="city"
            placeholder="Destination (e.g., Paris)"
            value={formData.city}
            onChange={handleInputChange}
            required
          />
          <input
            name="origin"
            placeholder="Origin Airport (e.g., JFK)"
            value={formData.origin}
            onChange={handleInputChange}
            required
          />
          <input
            name="travel_date"
            type="date"
            value={formData.travel_date}
            onChange={handleInputChange}
            required
          />
          <button type="submit" disabled={loading.main}>
            {loading.main ? 'Planning...' : 'Generate Trip Plan'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {Object.keys(serviceStatus).length > 0 && (
          <div className="service-status">
            <h3>Service Status:</h3>
            {Object.entries(serviceStatus).map(([service, status]) => (
              <p key={service}>
                {service}: <span style={{ color: getStatusColor(status) }}>
                  {status}
                </span>
              </p>
            ))}
          </div>
        )}

        {plan && (
          <div className="results">
            <div className="card summary-card">
              <h2>Your AI-Generated Trip Plan</h2>
              <div className="summary-content" style={{ whiteSpace: 'pre-line' }}>
                {plan.summary || "No summary available"}
              </div>
            </div>

            <div className="details-section">
              <div className="card">
                <h3>✈️ Flight Details</h3>
                {plan.raw_data?.flights?.length > 0 ? (
                  plan.raw_data.flights.map((flight, i) => (
                    <div key={i} className="flight-option">
                      <p><strong>{flight.airline} {flight.flight_number}</strong></p>
                      <p>{flight.departure_airport} → {flight.arrival_airport}</p>
                      <p>Departs: {flight.departure_time}</p>
                      <p>Arrives: {flight.arrival_time}</p>
                      <p>Status: {flight.status}</p>
                      {flight.source === 'mock' && <p className="mock-notice">Mock data</p>}
                    </div>
                  ))
                ) : (
                  <p>No flight information available</p>
                )}
              </div>

              <div className="card">
                <h3>🏛️ Recommended Activities</h3>
                {plan.raw_data?.activities?.length > 0 ? (
                  <ul>
                    {plan.raw_data.activities.map((activity, i) => (
                      <li key={i}>{activity}</li>
                    ))}
                  </ul>
                ) : (
                  <p>No activity suggestions available</p>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; */




























/* import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({ city: '', origin: '', travel_date: '' });
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPlan(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/plan_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setPlan(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Travel Planner</h1>
        <p>Let our AI agents plan your next trip!</p>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="trip-form">
          <input name="city" placeholder="Destination City (e.g., Paris)" onChange={handleInputChange} required />
          <input name="origin" placeholder="Origin Airport Code (e.g., DFW, JFK)" onChange={handleInputChange} required />
          <input name="travel_date" type="date" onChange={handleInputChange} required />
          <button type="submit" disabled={loading}>{loading ? 'Planning...' : 'Plan My Trip'}</button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {plan && (
          <div className="results">
            <h2>{plan.summary}</h2>

            <div className="card">
              <h3>✈️ Flight Options</h3>
              {plan.flight_details.flights.map((flight, index) => (
                <div key={index} className="flight-option">
                  <p><strong>Airline:</strong> {flight.airline} ({flight.flight_number})</p>
                  <p><strong>Departure:</strong> {flight.departure_airport}</p>
                  <p><strong>Arrival:</strong> {flight.arrival_airport}</p>
                  <p><strong>Status:</strong> {flight.status}</p>
                  <p><strong>Price:</strong> {flight.price_usd}</p>
                </div>
              ))}
            </div>
            
            <div className="card">
              <h3>🗺️ Tourist Attractions</h3>
              <ul>
                {plan.suggested_activities.map((activity, index) => (
                  <li key={index}>{activity}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; */




















/* import React, { useState } from 'react';
import './App.css';

function App() {
  const [formData, setFormData] = useState({ city: '', origin: '', travel_date: '' });
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPlan(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/plan_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setPlan(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Smart Travel Planner</h1>
        <p>Let our AI agents plan your next trip!</p>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="trip-form">
          <input name="city" placeholder="Destination City (e.g., Paris)" onChange={handleInputChange} required />
          <input name="origin" placeholder="Origin City (e.g., New York)" onChange={handleInputChange} required />
          <input name="travel_date" type="date" onChange={handleInputChange} required />
          <button type="submit" disabled={loading}>{loading ? 'Fetching...' : 'Flight Details for your Trip.'}</button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {plan && (
          <div className="results">
            <h2>{plan.summary}</h2>
            <div className="card">
              <h3>✈️ Flight Details</h3>
              <p><strong>Airline:</strong> {plan.flight_details.airline}</p>
              <p><strong>Price:</strong> ${plan.flight_details.price_usd}</p>
            </div>
            <div className="card">
              <h3>🗺️ Suggested Activities</h3>
              <ul>
                {plan.suggested_activities.map((activity, index) => (
                  <li key={index}>{activity}</li>
                ))}
              </ul>
            </div>
          </div> 
        )} 
      </main>
    </div>
  );
}

export default App; */
