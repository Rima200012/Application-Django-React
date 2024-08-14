import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

// Fallback base URL if not set in environment variables
const fallbackApiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

// Create an instance of axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || fallbackApiUrl,
});

// Add a request interceptor to include the Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
