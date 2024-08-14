import { createContext, useContext, useState, useEffect } from 'react';
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

  useEffect(() => {
    const checkAuth = async () => {
      const accessToken = localStorage.getItem(ACCESS_TOKEN);
      if (accessToken) {
        try {
          const userRes = await api.get('/users/users/me/', {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          const userData = userRes.data.user;
          setAuthState({
            authenticated: true,
            email: userData.email,
            id: userData.id,
            role: userData.role
          });
        } catch (error) {
          console.log(error);
        }
      }
    };
    checkAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const res = await api.post("/users/token/", { email, password });
      const { access, refresh } = res.data;
  
      localStorage.setItem(ACCESS_TOKEN, access);
      localStorage.setItem(REFRESH_TOKEN, refresh);
  
      // Fetch user details after login
      const userRes = await api.get("/users/users/me/", {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      });
      const userData = userRes.data.user;
  
      localStorage.setItem("role", userData.role);
      localStorage.setItem("userId", userData.id);
  
      setAuthState({
        authenticated: true,
        email: userData.email,
        id: userData.id,
        role: userData.role
      });
  
      return true;
    } catch (error) {
      // Remove the alert and return the error to be handled by the component
      throw error;  // This allows the error to be caught in the calling function
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
