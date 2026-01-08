import api from "../api";

export const listLocations = async (params) => {
    const { data } = await api.get('/locations/', { params });
    return Array.isArray(data) ? data : data.results;
}

export const getLocation = async (id) => {
    const { data } = await api.get(`/locations/${id}/`);
    return data;
}

export const createLocation = async (payload) => {
    const { data } = await api.post('/locations/', payload);
    return data;
}

export const updateLocation = async (id, payload) => {
    const { data } = await api.patch(`/locations/${id}/`, payload);
    return data;
}

export const deleteLocation = async (id) => {
    await api.delete(`/locations/${id}/`);
}
