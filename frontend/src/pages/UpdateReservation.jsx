import { React, useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom';
import ReservationForm from '../components/ReservationForm';
import LoadingIndicator from '../components/LoadingIndicator';
import Layout from '../components/Layout';
import { getReservation, updateReservation } from '../services/reservations';

function UpdateReservation() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [reservation, setReservation] = useState(null);

  useEffect(() => {
    (async () => {
      const r = await getReservation(id);
      setReservation({
        ...r,
        location_id: r.location_id ?? r.location?.id ?? null,
      });
    })();
  }, [id]);


  async function submit(data) {
    await updateReservation(id, data);
    navigate("/reservations");
  }
  
  if (!reservation) return <Layout><LoadingIndicator /></Layout>

  return (
    <Layout>
      <ReservationForm title="Update Reservation" submitLabel="Update" initialData={reservation} onSubmit={submit} />
    </Layout>
  );
}

export default UpdateReservation