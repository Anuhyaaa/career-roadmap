import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import { AuthProvider } from './contexts/AuthContext'
import ErrorBoundary from './components/ErrorBoundary'
import Home from './pages/Home'
import Results from './pages/Results'
import Login from './pages/Login'
import Signup from './pages/Signup'
import History from './pages/History'
import './App.css'

function App() {
  return (
    <Router>
      <AuthProvider>
        <ErrorBoundary>
          <Layout>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/results" element={<Results />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/history" element={<History />} />
            </Routes>
          </Layout>
        </ErrorBoundary>
      </AuthProvider>
    </Router>
  )
}

export default App