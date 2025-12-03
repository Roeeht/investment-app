import axios from "axios";

const BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

// Stock API calls
export const stockAPI = {
  getStock: (symbol) => api.get(`/stock?symbol=${symbol}`),
};

// User API calls (when implemented)
export const userAPI = {
  register: (userData) => api.post("/users/register", userData),
  login: (credentials) => api.post("/users/login", credentials),
  getProfile: () => api.get("/users/profile"),
};

// Portfolio API calls (when implemented)
export const portfolioAPI = {
  getPortfolio: () => api.get("/portfolio"),
  getPurchases: () => api.get("/purchases"),
  getDeposits: () => api.get("/deposits"),
};

export default api;
