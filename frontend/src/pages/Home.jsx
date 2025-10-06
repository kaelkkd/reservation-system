import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Layout from "../components/Layout";
import Card from "../components/Card";
import Button from "../components/Button";
import Table from "../components/Table";
import { listReservations } from "../services/reservations";
import { listLocations } from "../services/locations";
import "../styles/Home.css";

export default function Home() {
  const [reservations, setReservations] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const [resv, locs] = await Promise.all([
          listReservations().then(r => (Array.isArray(r) ? r : r.results || [])),
          listLocations({ limit: 5 }).then(r => (Array.isArray(r) ? r : r.results || [])),
        ]);
        setReservations(resv.slice(0, 5));
        setLocations(locs.slice(0, 5));
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const reservationColumns = [
    { header: "Location", render: r => r.location?.name || "-" },
    { header: "From", accessor: "start_date" },
    { header: "To", accessor: "end_date" },
    { header: "People", accessor: "number_of_people" },
  ];

  return (
    <Layout>
      <section className="home-hero">
        <div className="hero-copy">
          <h1>Book your next space with ease</h1>
          <p>Find available locations and manage your reservations in one place.</p>
          <div className="hero-actions">
            <Link to="/locations"><Button>Browse Locations</Button></Link>
            <Link to="/reservations/new"><Button variant="ghost">New Reservation</Button></Link>
          </div>
        </div>
        <div className="hero-card">
          <Card header="Quick Links">
            <div className="quick-grid">
              <Link to="/locations" className="quick-link">All Locations →</Link>
              <Link to="/reservations" className="quick-link">My Reservations →</Link>
              <Link to="/reservations/new" className="quick-link">Create Reservation →</Link>
            </div>
          </Card>
        </div>
      </section>

      <div className="home-grid">
        <Card header="Recent Reservations" footer={<Link to="/reservations" className="card-link">View all →</Link>}>
          {loading ? "Loading..." : (
            <Table columns={reservationColumns} rows={reservations} empty="No recent reservations." />
          )}
        </Card>

        <Card header="Popular Locations" footer={<Link to="/locations" className="card-link">Explore →</Link>}>
          {loading ? "Loading..." : (
            <ul className="loc-list">
              {locations.length === 0 ? <li className="muted">No locations yet.</li> : locations.map(l => (
                <li key={l.id} className="loc-item">
                  <div className="loc-name">{l.name}</div>
                  <div className="loc-meta">{l.country} • Max. cap. {l.capacity}</div>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </Layout>
  );
}