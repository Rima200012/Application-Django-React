import React from 'react';

const startAuth = () => {
  window.location.href = 'http://127.0.0.1:8000/start_auth/';
};

const Auth = () => {
  return (
    <div>
      <button onClick={startAuth}>Login with Power BI</button>
    </div>
  );
};

export default Auth;
