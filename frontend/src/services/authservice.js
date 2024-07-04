import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

const login = async (username, password) => {
  const response = await axios.post(API_URL + 'login/', {
    username,
    password,
  });
  if (response.data.access) {
    localStorage.setItem('user', JSON.stringify(response.data));
  }
  return response.data;
};

const authService = {
  login,
};

export default authService;
