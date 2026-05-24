// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const getRecommendations = async (text) => {
  try {
    const response = await api.post('/recommend', { text });
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

export const getMoods = async () => {
  try {
    const response = await api.get('/moods');
    return response.data;
  } catch (error) {
    console.error('Error getting moods:', error);
    throw error;
  }
};

export const getFoodByMood = async (mood, limit = 3) => {
  try {
    const response = await api.get(`/food/${mood}?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error getting food by mood:', error);
    throw error;
  }
};

export const getMusicByMood = async (mood, limit = 3) => {
  try {
    const response = await api.get(`/music/${mood}?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error getting music by mood:', error);
    throw error;
  }
};

export const getRecipeDetails = async (foodName) => {
  try {
    const response = await api.get(`/recipe/${encodeURIComponent(foodName)}`);
    return response.data;
  } catch (error) {
    console.error('Error getting recipe details:', error);
    throw error;
  }
};

export default api;