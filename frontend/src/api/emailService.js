import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchEmails = async () => {
  const response = await axios.get(`${API_URL}/mails`);
  return response.data;
};
