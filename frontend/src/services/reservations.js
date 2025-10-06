import api from "../api";

export const listReservations = async () => {
    const { data } = await api.get('/reserve/');
    return Array.isArray(data) ? data : (data.results || []); 
}

export const getReservation = async (id) => {
    const { data } = await api.get(`/reserve/${id}/`);
    return data;
}

export const postReservation = async (payload) => {
    const { data } = await api.post('/reserve/', payload);
    return data;
}

export const cancelReservation = async (id) => {
    await api.delete(`/reserve/${id}/`);
}