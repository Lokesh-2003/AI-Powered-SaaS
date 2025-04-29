import { create } from 'zustand';
import jwtDecode from 'jwt-decode';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const useAuthStore = create((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const response = await axios.post(`${API_URL}/api/v1/auth/login`, {
        username: email,
        password,
      });
      const { access_token } = response.data;
      const user = jwtDecode(access_token);
      
      set({
        user,
        token: access_token,
        isAuthenticated: true,
        loading: false,
      });
      
      // Store token in localStorage
      localStorage.setItem('token', access_token);
      
      return true;
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Login failed',
        loading: false,
      });
      return false;
    }
  },

  register: async (email, password, fullName) => {
    set({ loading: true, error: null });
    try {
      await axios.post(`${API_URL}/api/v1/auth/register`, {
        email,
        password,
        full_name: fullName,
      });
      set({ loading: false });
      return true;
    } catch (error) {
      set({
        error: error.response?.data?.detail || 'Registration failed',
        loading: false,
      });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    });
  },

  initialize: () => {
    const token = localStorage.getItem('token');
    if (token) {
      const user = jwtDecode(token);
      set({
        user,
        token,
        isAuthenticated: true,
      });
    }
  },
}));

export default useAuthStore;