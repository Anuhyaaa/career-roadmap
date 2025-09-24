﻿﻿﻿import { createContext, useContext, useState, useEffect } from 'react'
import { API_BASE_URL } from '../config/api'

const AuthContext = createContext()

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    // Check if user is already logged in on app start
    useEffect(() => {
        checkAuthStatus()
    }, [])

    const checkAuthStatus = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            })

            if (response.ok) {
                const userData = await response.json()
                setIsAuthenticated(true)
                setUser(userData)
            } else {
                setIsAuthenticated(false)
                setUser(null)
            }
        } catch (error) {
            console.error('Auth check failed:', error)
            setIsAuthenticated(false)
            setUser(null)
        } finally {
            setLoading(false)
        }
    }

    const login = async (email, password) => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password })
            })

            const data = await response.json()

            if (response.ok) {
                setIsAuthenticated(true)
                setUser(data.user)
                return { success: true }
            } else {
                return { 
                    success: false, 
                    error: data.error || 'Login failed' 
                }
            }
        } catch (error) {
            console.error('Login error:', error)
            return { 
                success: false, 
                error: 'Network error. Please check your connection.' 
            }
        }
    }

    const register = async (email, password, fullName) => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    email, 
                    password, 
                    full_name: fullName 
                })
            })

            const data = await response.json()

            if (response.ok) {
                setIsAuthenticated(true)
                setUser(data.user)
                return { success: true }
            } else {
                return { 
                    success: false, 
                    error: data.error || 'Registration failed' 
                }
            }
        } catch (error) {
            console.error('Registration error:', error)
            return { 
                success: false, 
                error: 'Network error. Please check your connection.' 
            }
        }
    }

    const logout = async () => {
        try {
            await fetch(`${API_BASE_URL}/auth/logout`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
        } catch (error) {
            console.error('Logout error:', error)
        } finally {
            setIsAuthenticated(false)
            setUser(null)
        }
    }

    return (
        <AuthContext.Provider value={{ 
            isAuthenticated, 
            user, 
            login, 
            register, 
            logout, 
            loading 
        }}>
            {children}
        </AuthContext.Provider>
    )
}
