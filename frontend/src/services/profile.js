import api from "../api";

export const getProfile = async () => {
    const { data } = await api.get('/api/profiles/me/');
    return data;
}

export const updateProfile = async (payload) => {
    const { data } = await api.patch('/api/profiles/me/', payload);
    return data;
}

export const putProfile = async (payload) => {
    const { data } = await api.put('/api/profiles/me/', payload);
    return data;
}