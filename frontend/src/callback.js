import React, { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Callback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTokens = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');

      try {
        const response = await axios.get(`http://127.0.0.1:8000/auth_callback?code=${code}`);
        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        // Redirect to dashboard or home page
        navigate('/candidate-home'); // Adjust this based on where you want to navigate after login
      } catch (error) {
        console.error('Error fetching tokens:', error);
      }
    };

    fetchTokens();
  }, [navigate]);

  return <div>Logging in...</div>;
};

export default Callback;
