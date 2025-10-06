import { useEffect, useState } from 'react'
import Layout from "../components/Layout"
import Card from "../components/Card"
import Button from "../components/Button"
import { Field, Input, Select} from "../components/Field"
import { listLocations } from "../services/locations"
import { postReservation } from "../services/reservations"
import { useNavigate } from "react-router-dom"

function NewReservation() {
  const [locations, setLocations] = useState([]);
  const [form, setForm] = useState({ location_id: "", start_date: "", end_date: "", number_of_people: 1 });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  useEffect(() => { (async () => setLocations(await listLocations()))(); }, []);

  async function submit(e) {
    e.preventDefault();
    setErrors({});
    try {
      await postReservation(form);
      navigate("/reservations");
    } catch (err) {
      const apiErrors = err?.response?.data || {};
      setErrors(apiErrors);
    }
  }

  return (
    <Layout>
      <Card header="Create Reservation">
        <form className='form' onSubmit={submit}>
          <Field label="Location" error={errors.location || errors.location_id}>
            <Select required value={form.location_id} onChange={e => setForm({ ...form, location_id: e.target.value })}>
              <option value="" disabled>Select a location</option>
              {locations.map(l => <option key={l.id} value={l.id}>{l.name} - cap {l.capacity}</option>)}
            </Select>
          </Field>

          <Field label="Start date" error={errors.start_date}>
            <Input type="date" required value={form.start_date} onChange={e => setForm({ ...form, start_date: e.target.value })}/>
          </Field>

          <Field label="End date" error={errors.end_date}>
            <Input type="date" required value={form.end_date} onChange={e => setForm({ ...form, end_date: e.target.value })}/>
          </Field>

          <Field label="Number of people" error={errors.number_of_people}>
            <Input type="number" min="1" required value={form.number_of_people} 
              onChange={e => setForm({ ...form, number_of_people: Number(e.target.value) })}/>
          </Field>
          
          {errors.non_fiel_errors ? <div style={{ color: "var(--danger)" }}>{errors.non_fiel_errors}</div> : null}

          <div style={{display: "flex", gap: 10, marginTop: 6}}>
            <Button type="submit">Create</Button>
            <Button type="button" variant="ghost" onClick={() => navigate(-1)}>Cancel</Button>
          </div>
        </form>
      </Card>
    </Layout>
  );
}

export default NewReservation