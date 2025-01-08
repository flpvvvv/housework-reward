import axios from 'axios';

const api = axios.create({
  baseURL: window._env_?.REACT_APP_BACKEND_URL || 'http://localhost:8000/api',
});

export const minioEndpoint = window._env_?.REACT_APP_MINIO_ENDPOINT || 'http://localhost:9000';

export default api;