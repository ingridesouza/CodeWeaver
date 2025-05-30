import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
});

export async function generatePrompt(prompt) {
  const response = await apiClient.post('/generate/', { prompt });
  return response.data;
}
