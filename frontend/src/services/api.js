import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api', // backend URL
});

export const fetchNotes = () => api.get('/notes/');
export const createNote = (noteData) => api.post('/notes/', noteData);