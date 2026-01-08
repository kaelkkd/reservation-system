import Layout from "../components/Layout"
import ReservationForm from '../components/ReservationForm'
import { postReservation } from "../services/reservations"
import { useNavigate } from "react-router-dom"

function NewReservation() {
  const navigate = useNavigate();

  async function createReservation(data) {
    await postReservation(data);
    navigate("/reservations");
  }

  return (
    <Layout>
      <ReservationForm title="Create Reservation" submitLabel="Create" initialData={{location_id: null, start_date: "", 
        end_date: "", number_of_people: 1,}} onSubmit={createReservation} />
    </Layout>
  );
}

export default NewReservation