import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import Table from "../components/Table";
import Button from "../components/Button";
import { listReservations, cancelReservation } from "../services/reservations";

function Reservations() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    try { setRows(await listReservations()); }
    finally { setLoading(false); }
  }

  useEffect(() => { load(); }, []);

  const columns = [
    { header: "Location", render: r => r.location?.name || "-" },
    { header: "From", accessor: "start_date" },
    { header: "To", accessor: "end_date" },
    { header: "People", accessor: "number_of_people" },
    { header: "Reserved at", accessor: "reserved_at" },
    { header: "", render: (r) => (
      <Button variant="danger" onClick={async () => {
        await cancelReservation(r.reservation_id);
        await load();
      }}>Cancel</Button>
    )}
  ];

  return (
    <Layout>
      <h1>My Reservations</h1>
      <div style={{ marginTop: 16 }}>
        {loading ? "Loading..." : <Table columns={columns} rows={rows} empty="No reservations yet." />}
      </div>
    </Layout>
  );
}

export default Reservations