import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const testConnection = async (config) => {
  const response = await api.post('/api/test-connection', { config });
  return response.data;
};

export const generateTestCases = async (config, issueId) => {
  const response = await api.post('/api/generate', {
    config,
    issue_id: issueId,
  });
  return response.data;
};

export default api;
