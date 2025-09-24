// API Configuration
const getApiBaseUrl = () => {
  // Check if we're in development mode
  if (import.meta.env.DEV) {
    return 'http://localhost:5000/api'
  }
  
  // Production API URL (will be updated after backend deployment)
  return import.meta.env.VITE_API_BASE_URL || 'https://your-backend-url.vercel.app/api'
}

export const API_BASE_URL = getApiBaseUrl()