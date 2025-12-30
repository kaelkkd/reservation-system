import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Card from "../components/Card"
import LoadingIndicator from "../components/LoadingIndicator"
import Button from "../components/Button"
import { getProfile, updateProfile } from '../services/profile'
import { Field, Input, Select } from '../components/Field'
import Layout from '../components/Layout'

function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();
  const [form, setForm] = useState({display_name: "", address_line: "", country: "BR", bio: ""});

  useEffect(() => { const fetchProfile = async () => { 
        try {
          setLoading(true);
          const data = await getProfile();
          setProfile(data);
          setForm({display_name: data.display_name ?? "", address_line: data.address_line ?? "",
                    country: data.country ?? "BR", bio: data.bio ?? ""});
        } catch (err) {
          console.error("Failed to fetch profile:", err);
        } finally {
          setLoading(false);
        }
      };
    fetchProfile();
  }, []);

  async function submit(e) {
    e.preventDefault();
    setErrors({});
    setSaving(true);
    try {
      const updated = await updateProfile(form);
      setProfile(updated);

    } catch (err) {
      const apiErrors = err?.response?.data || {};
      setErrors(apiErrors);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <Layout><LoadingIndicator /></Layout>;
  }

  return (
    <Layout>
      <Card header="Profile">
        <form className="form" onSubmit={submit}>
          <Field label="Display name" error={errors.display_name}>
            <Input type="text" required value={form.display_name} onChange={e => setForm({ ...form, display_name: e.target.value })}></Input>
          </Field>

          <Field label="Email">
            <Input value={profile?.email ?? ""} disabled></Input>
          </Field>

          <Field label="Address line" error={errors.address_line}>
            <Input type="text" required value={form.address_line} onChange={e => setForm({ ...form, address_line: e.target.value })}></Input>
          </Field>

          <Field label="Country" error={errors.country}>
            <Select value={form.country} onChange={e => setForm({ ...form, country: e.target.value })}>
              <option value="BR">Brazil</option>
              <option value="US">United States</option>
              <option value="UK">United Kingdom</option>
              <option value="ES">Spain</option>
              <option value="JP">Japan</option>
              <option value="AU">Australia</option>
            </Select>
          </Field>

          <Field label="Bio" error={errors.bio}>
            <Input type="text" required value={form.bio} onChange={e => setForm({ ...form, bio: e.target.value })} maxLength={300}></Input>
          </Field>

          {errors.non_field_errors && (<div style={{ color: "var(--danger)" }}>{errors.non_field_errors}</div>)}
          <div style={{ display: "flex", gap: 10, marginTop: 6 }}>
            <Button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Save changes"}
            </Button>
            {saving && <LoadingIndicator />}
          </div> 

        </form>
      </Card>
    </Layout>
  )
}

export default Profile