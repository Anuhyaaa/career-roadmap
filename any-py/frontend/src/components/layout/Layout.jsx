import { Link, useLocation } from 'react-router-dom'
import { LogOut, History, Sparkles, Menu, X, Heart } from 'lucide-react'
import { useState } from 'react'
import { Button } from '../ui/Button'
import { useAuth } from '../../contexts/AuthContext'

const Layout = ({ children }) => {
  const location = useLocation()
  const { isAuthenticated, user, logout, loading } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const scrollToForm = () => {
    const formSection = document.getElementById('design-form')
    if (formSection) {
      formSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50 backdrop-blur-sm bg-white/95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="relative">
                <Sparkles className="h-7 w-7 sm:h-8 sm:w-8 text-gray-900 group-hover:text-blue-600 transition-colors duration-200" />
                <div className="absolute inset-0 bg-blue-600 rounded-full opacity-0 group-hover:opacity-10 transition-opacity duration-200 transform scale-110"></div>
              </div>
              <span className="text-lg sm:text-xl font-semibold text-gray-900 tracking-tight">
                <span className="hidden sm:inline">Career Roadmap</span>
                <span className="sm:hidden">Roadmap</span>
              </span>
            </Link>

            {/* Desktop Navigation Links */}
            <div className="hidden md:flex items-center space-x-1">
              {location.pathname === '/' ? (
                <button
                  onClick={scrollToForm}
                  className="px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 text-blue-600 bg-blue-50 hover:bg-blue-100"
                >
                  Generate
                </button>
              ) : (
                <Link
                  to="/"
                  className="px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                >
                  Generate
                </Link>
              )}

              {isAuthenticated && (
                <Link
                  to="/history"
                  className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2 ${location.pathname === '/history'
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                >
                  <History className="h-4 w-4" />
                  <span>History</span>
                </Link>
              )}
            </div>

            {/* Desktop Auth Actions */}
            <div className="hidden sm:flex items-center space-x-3">
              {isAuthenticated ? (
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 rounded-lg">
                    <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                      {user?.avatar}
                    </div>
                    <span className="text-sm font-medium text-gray-700 hidden lg:inline">
                      {user?.name}
                    </span>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-gray-600 hover:text-gray-900"
                    onClick={logout}
                  >
                    <LogOut className="h-4 w-4" />
                  </Button>
                </div>
              ) : (
                <div className="flex items-center space-x-3">
                  <Link to="/login">
                    <Button variant="ghost" size="sm">
                      Sign In
                    </Button>
                  </Link>
                  <Link to="/signup">
                    <Button size="sm">
                      Get Started
                    </Button>
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="sm:hidden flex items-center">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
              >
                <span className="sr-only">Open main menu</span>
                {mobileMenuOpen ? (
                  <X className="block h-6 w-6" />
                ) : (
                  <Menu className="block h-6 w-6" />
                )}
              </button>
            </div>
          </div>

          {/* Mobile menu */}
          <div className={`sm:hidden ${mobileMenuOpen ? 'block' : 'hidden'} pb-4 border-t border-gray-200`}>
            <div className="pt-4 space-y-2">
              {location.pathname === '/' ? (
                <button
                  onClick={() => {
                    scrollToForm()
                    setMobileMenuOpen(false)
                  }}
                  className="block w-full text-left px-3 py-2 text-base font-medium rounded-lg transition-colors duration-200 text-blue-600 bg-blue-50 hover:bg-blue-100"
                >
                  Generate Roadmap
                </button>
              ) : (
                <Link
                  to="/"
                  className="block px-3 py-2 text-base font-medium rounded-lg transition-colors duration-200 text-gray-600 hover:text-gray-900 hover:bg-gray-50"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Generate Roadmap
                </Link>
              )}

              {isAuthenticated && (
                <Link
                  to="/history"
                  className={`block px-3 py-2 text-base font-medium rounded-lg transition-colors duration-200 ${location.pathname === '/history'
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <div className="flex items-center space-x-2">
                    <History className="h-5 w-5" />
                    <span>My History</span>
                  </div>
                </Link>
              )}
            </div>

            {/* Mobile Auth Section */}
            <div className="pt-4 mt-4 border-t border-gray-200">
              {isAuthenticated ? (
                <div className="space-y-3">
                  <div className="flex items-center px-3 py-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-medium mr-3">
                      {user?.avatar}
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-900">{user?.name}</div>
                      <div className="text-xs text-gray-500">{user?.email}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      logout()
                      setMobileMenuOpen(false)
                    }}
                    className="w-full flex items-center px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                  >
                    <LogOut className="h-5 w-5 mr-2" />
                    Sign Out
                  </button>
                </div>
              ) : (
                <div className="space-y-2">
                  <Link
                    to="/login"
                    className="block w-full text-center px-3 py-2 text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Sign In
                  </Link>
                  <Link
                    to="/signup"
                    className="block w-full text-center px-3 py-2 text-base font-medium text-white bg-gray-900 hover:bg-gray-800 rounded-lg transition-colors duration-200"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Get Started
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Minimalist Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16 sm:mt-20 lg:mt-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
          <div className="flex flex-col items-center text-center space-y-6">
            {/* Logo and tagline */}
            <div className="flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-blue-600" />
              <span className="text-xl font-semibold text-gray-900 tracking-tight">
                Career Roadmap Generator
              </span>
            </div>

            <p className="text-sm text-gray-600 max-w-lg leading-relaxed">
              AI-powered career planning for ambitious professionals.
              Transform your aspirations into actionable roadmaps.
            </p>

            {/* Simple navigation */}
            <div className="flex flex-wrap justify-center gap-6 text-sm">
              {location.pathname === '/' ? (
                <button
                  onClick={scrollToForm}
                  className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium"
                >
                  Generate Roadmap
                </button>
              ) : (
                <Link to="/" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                  Generate Roadmap
                </Link>
              )}
              {isAuthenticated && (
                <Link to="/history" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                  My History
                </Link>
              )}
              <Link to="/privacy" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 font-medium">
                Privacy
              </Link>
            </div>

            {/* Built by and copyright */}
            <div className="pt-6 border-t border-gray-100 w-full">
              <div className="flex flex-col sm:flex-row justify-between items-center space-y-3 sm:space-y-0">
                <div className="flex items-center space-x-1 text-sm text-gray-500">
                  <span>Built with</span>
                  <Heart className="h-4 w-4 text-red-500 fill-current" />
                  <span>by</span>
                  <span className="font-medium text-blue-600">Anuhya</span>
                </div>

                <p className="text-sm text-gray-500">
                  © 2025 Career Roadmap Generator
                </p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout