import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Card from "../components/Card";
import Button from "../components/Button";
import { listLocations } from "../services/locations";
import "../styles/Locations.css";

export default function Locations() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try { setItems(await listLocations()); }
      finally { setLoading(false); }
    })();
  }, []);

  return (
    <Layout>
      <div className="page-head">
        <h1>Locations</h1>
        <div className="page-actions">
          {/* Show only if admin */}
          {/* <Button onClick={() => setOpen(true)}>Add location</Button> */}
        </div>
      </div>

      {loading ? <div className="skeleton-grid">
        {Array.from({ length: 6 }).map((_, i) => <div className="skeleton-card" key={i} />)}
      </div> : (
        <div className="grid">
          {items.map(loc => (
            <Card key={loc.id}
              header={<div className="loc__header">
                <span className="loc__name">{loc.name}</span>
                <span className="loc__cap">{loc.capacity} people</span>
              </div>}
              footer={<div className="loc__footer">
                <span className="loc__country">{loc.country}</span>
                {/* admin actions here */}
              </div>}
            >
              <div className="loc__body">
                <div className="loc__addr">{loc.address}</div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </Layout>
  );
}