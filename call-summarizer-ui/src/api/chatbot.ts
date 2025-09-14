
import axios from 'axios';

export const sendChatRequest = async (formData: FormData) => {
  const response = await axios.post('/api/chatbot', formData);
  return response.data;
};
