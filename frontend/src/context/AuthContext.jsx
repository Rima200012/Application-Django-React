import { createContext, useContext, useState } from 'react';
import api from '../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';

export const Role = {
  RECRUITER: 'recruiter',
  CANDIDATE: 'candidate'
};

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState({
    authenticated: false,
    email: null,
    id: null,
    role: null
  });

  const login = async (email, password) => {
    try {
      const res = await api.post("/users/token/", { email, password });
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

      // Fetch user details after login
      const userRes = await api.get("/users/users/me/", {
        headers: {
          Authorization: `Bearer ${res.data.access}`,
        },
      });
      const userData = userRes.data.user;
      console.log("User data from backend:", userData); // Debug log

      localStorage.setItem("role", userData.role);
      localStorage.setItem("userId", userData.id);

      setAuthState({
        authenticated: true,
        email: userData.email,
        id: userData.id,
        role: userData.role
      });
      console.log("Auth state after login:", authState); // Debug log
      return true;
    } catch (error) {
      alert("Login failed: " + error.message);
      return false;
    }
  };

  const logout = () => {
    localStorage.clear();
    setAuthState({
      authenticated: false,
      email: null,
      id: null,
      role: null
    });
  };

  return (
    <AuthContext.Provider value={{ authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
