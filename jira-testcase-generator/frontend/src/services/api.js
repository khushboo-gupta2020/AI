import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const testConnection = async (config) => {
  const response = await api.post('/jira/test-connection', config);
  return response.data;
};

export const fetchStory = async (data) => {
  const response = await api.post('/jira/fetch-story', data);
  return response.data;
};

export const generateTestCases = async (data) => {
  const response = await api.post('/testcases/generate', data);
  return response.data;
};

export default api;
