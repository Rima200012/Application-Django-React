import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const EmailVerification = () => {
  const { uid, token } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/users/verify_email/${uid}/${token}/`);
        if (response.status === 200) {
          alert('Email verified successfully.');
          navigate('/login');
        } else {
          alert('Verification failed. Please try again.');
        }
      } catch (error) {
        alert('An error occurred during verification.');
      }
    };

    verifyEmail();
  }, [uid, token, navigate]);

  return <div>Verifying your email...</div>;
};

export default EmailVerification;
