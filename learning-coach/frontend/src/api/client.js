import axios from 'axios'

// All API calls go to backend — API key is NEVER in frontend
const api = axios.create({ baseURL: 'http://localhost:8000' })

export const generateQuestion = (userId, topic) =>
  api.post('/api/generate-question', { user_id: userId, topic })

export const submitAnswer = (data) => api.post('/api/submit-answer', data)

export const getExplanation = (topic, level = 'intermediate') =>
  api.get('/api/explanation', { params: { topic, level } })

export const getProgress = (userId) => api.get(`/api/progress/${userId}`)

export const getAnalytics = (userId) => api.get(`/api/analytics/${userId}`)

export const getLearningPath = (userId) => api.get(`/api/learning-path/${userId}`)

export const sendChat = (userId, message, topic, mode = 'tutor') =>
  api.post('/api/chat', { user_id: userId, message, current_topic: topic, mode })

export const getTopics = () => api.get('/api/topics')
