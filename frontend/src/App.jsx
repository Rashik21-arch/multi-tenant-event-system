import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [analytics, setAnalytics] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [analyticsResponse, eventsResponse] = await Promise.all([
          fetch(`${API}/analytics/`),
          fetch(`${API}/events/`)
        ]);

        const analyticsData = await analyticsResponse.json();
        const eventsData = await eventsResponse.json();

        setAnalytics(analyticsData);
        setEvents(eventsData);
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>🎟️ Event Reservation System</h1>
          <p>Multi-Tenant Event & Ticket Management Platform</p>
        </div>

        <div className="status">
          <span></span> Backend Connected
        </div>
      </header>

      <main className="container">

        <h2>Analytics Dashboard</h2>

        <div className="cards">

          <div className="card">
            <div className="icon">🎫</div>
            <div>
              <p>Total Reservations</p>
              <h3>{analytics?.total_reservations ?? 0}</h3>
            </div>
          </div>

          <div className="card">
            <div className="icon">✅</div>
            <div>
              <p>Confirmed</p>
              <h3>{analytics?.confirmed_reservations ?? 0}</h3>
            </div>
          </div>

          <div className="card">
            <div className="icon">⏳</div>
            <div>
              <p>Held</p>
              <h3>{analytics?.held_reservations ?? 0}</h3>
            </div>
          </div>

          <div className="card">
            <div className="icon">❌</div>
            <div>
              <p>Expired</p>
              <h3>{analytics?.expired_reservations ?? 0}</h3>
            </div>
          </div>

          <div className="card revenue">
            <div className="icon">₹</div>
            <div>
              <p>Total Revenue</p>
              <h3>₹{analytics?.revenue ?? 0}</h3>
            </div>
          </div>

          <div className="card">
            <div className="icon">📈</div>
            <div>
              <p>Conversion Rate</p>
              <h3>{analytics?.conversion_rate ?? 0}%</h3>
            </div>
          </div>

        </div>

        <section className="events-section">
          <h2>Available Events</h2>

          {events.length === 0 ? (
            <p className="empty">No events available.</p>
          ) : (
            <div className="events">

              {events.map((event) => (
                <div className="event-card" key={event.id}>

                  <div className="event-top">
                    <span className="event-id">
                      Event #{event.id}
                    </span>

                    <span className="tenant">
                      Tenant #{event.tenant_id}
                    </span>
                  </div>

                  <h3>{event.name}</h3>

                  <p>{event.description}</p>

                  <div className="event-info">
                    <span>📍 {event.location}</span>
                    <span>
                      📅 {new Date(event.event_date).toLocaleDateString()}
                    </span>
                  </div>

                </div>
              ))}

            </div>
          )}
        </section>

      </main>

      <footer>
        Multi-Tenant Event & Ticket Reservation System
      </footer>
    </div>
  );
}

export default App;