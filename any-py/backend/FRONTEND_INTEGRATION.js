// Frontend Integration Guide for Career Roadmap Generator Backend

// 1. Update your React frontend to use the new backend APIs
// Replace the mock API calls in your components with these real calls:

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    credentials: 'include', // Important for session cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// 2. Update Home.jsx - Replace the mock roadmap generation
// In your Home.jsx handleRoadmapSubmit function:

const handleRoadmapSubmit = async (formData) => {
  setLoading(true);

  try {
    // Call the real backend API
    const response = await apiCall('/api/generate-roadmap', {
      method: 'POST',
      body: JSON.stringify(formData),
    });

    // Navigate to results with real data
    navigate('/results', {
      state: {
        formData,
        roadmap: response.roadmap,
        roadmapId: response.roadmap_id,
        saved: response.saved
      }
    });
  } catch (error) {
    console.error('Error generating roadmap:', error);
    // Handle error - show user-friendly message
    alert('Failed to generate roadmap. Please try again.');
  } finally {
    setLoading(false);
  }
};

// 3. Update Login.jsx - Replace mock login
// In your Login.jsx handleSubmit function:

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validateForm()) return;

  setLoading(true);

  try {
    const response = await apiCall('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(formData),
    });

    // Update auth context with real user data
    login(response.user);
    
    // Navigate to home page on success
    navigate('/');
  } catch (error) {
    setErrors({ general: error.message });
  } finally {
    setLoading(false);
  }
};

// 4. Update Signup.jsx - Replace mock registration
// In your Signup.jsx handleSubmit function:

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validateForm()) return;

  setLoading(true);

  try {
    const response = await apiCall('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(formData),
    });

    // Update auth context with real user data
    login(response.user);
    
    // Navigate to home page on success
    navigate('/');
  } catch (error) {
    setErrors({ general: error.message });
  } finally {
    setLoading(false);
  }
};

// 5. Update AuthContext.jsx - Add real authentication
// Replace your AuthContext with real API calls:

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check authentication status on app load
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await apiCall('/api/auth/check-session');
      if (response.authenticated) {
        setIsAuthenticated(true);
        setUser(response.user);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
  };

  const logout = async () => {
    try {
      await apiCall('/api/auth/logout', {
        method: 'POST',
      });
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      isAuthenticated, 
      user, 
      login, 
      logout, 
      loading 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// 6. Create History.jsx - Add roadmap history functionality
// Create a new component to show user's roadmap history:

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const History = () => {
  const [roadmaps, setRoadmaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadRoadmapHistory();
  }, []);

  const loadRoadmapHistory = async () => {
    try {
      const response = await apiCall('/api/roadmaps/history');
      setRoadmaps(response.roadmaps);
    } catch (error) {
      setError('Failed to load roadmap history');
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const viewRoadmap = (roadmapId) => {
    navigate(`/roadmap/${roadmapId}`);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Your Roadmap History</h1>
      
      {roadmaps.length === 0 ? (
        <p>No roadmaps found. Generate your first roadmap!</p>
      ) : (
        <div className="space-y-4">
          {roadmaps.map((roadmap) => (
            <div key={roadmap.id} className="border rounded-lg p-4">
              <h3 className="font-semibold">{roadmap.roadmap_summary.career_goal}</h3>
              <p className="text-gray-600">
                Created: {new Date(roadmap.created_at).toLocaleDateString()}
              </p>
              <p className="text-sm text-gray-500">
                {roadmap.roadmap_summary.total_skills} skills • 
                {roadmap.roadmap_summary.estimated_weeks} weeks
              </p>
              <button 
                onClick={() => viewRoadmap(roadmap.id)}
                className="mt-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                View Roadmap
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;

// 7. Update Results.jsx - Add PDF export functionality
// Add a function to export roadmap as PDF:

const exportToPDF = async (roadmapId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/pdf/export/${roadmapId}`, {
      credentials: 'include',
    });
    
    if (!response.ok) {
      throw new Error('Failed to export PDF');
    }
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `career_roadmap_${roadmapId}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  } catch (error) {
    console.error('Export failed:', error);
    alert('Failed to export PDF. Please try again.');
  }
};

// 8. Testing Steps:

// 1. Start the backend server:
//    cd c:\anuhya\python-project\new-python-project\any-py\backend
//    .\venv\Scripts\python.exe simple_server.py

// 2. Update your React components with the code above

// 3. Start your React frontend:
//    npm run dev

// 4. Test the integration:
//    - Try generating a roadmap (guest mode)
//    - Register a new user
//    - Login with the user
//    - Generate a roadmap (authenticated mode)
//    - View roadmap history

// The backend is fully functional and ready for integration!