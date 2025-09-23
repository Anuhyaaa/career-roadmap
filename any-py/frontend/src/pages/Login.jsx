import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card'
import { Sparkles, ArrowLeft, User, Lock } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Login = () => {
    const navigate = useNavigate()
    const { login } = useAuth()
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    })
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)

    const handleInputChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))

        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }))
        }
    }

    const validateForm = () => {
        const newErrors = {}

        if (!formData.email.trim()) {
            newErrors.email = 'Email is required'
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Please enter a valid email'
        }

        if (!formData.password) {
            newErrors.password = 'Password is required'
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!validateForm()) return

        setLoading(true)

        try {
            const result = await login(formData.email, formData.password)

            if (result.success) {
                // Navigate to home page on success
                navigate('/')
            } else {
                setErrors({ general: result.error })
            }
        } catch (error) {
            setErrors({ general: 'Login failed. Please try again.' })
        } finally {
            setLoading(false)
        }
    }

    const handleDemoLogin = async () => {
        setLoading(true)
        setFormData({ email: 'demo@example.com', password: 'demo123' })

        try {
            const result = await login('demo@example.com', 'demo123')
            if (result.success) {
                navigate('/')
            } else {
                setErrors({ general: result.error })
            }
        } catch (error) {
            setErrors({ general: 'Demo login failed. Please try again.' })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center py-8 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full">
                {/* Back button */}
                <div className="mb-4 sm:mb-6">
                    <Button
                        variant="ghost"
                        onClick={() => navigate('/')}
                        className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        <span>Back to Home</span>
                    </Button>
                </div>

                <Card className="animate-fade-in">
                    <CardHeader className="text-center px-4 sm:px-6">
                        <div className="flex justify-center mb-4">
                            <div className="relative">
                                <div className="absolute inset-0 bg-blue-600 rounded-full opacity-10 animate-pulse"></div>
                                <Sparkles className="h-8 w-8 sm:h-10 sm:w-10 text-blue-600 relative z-10" />
                            </div>
                        </div>
                        <CardTitle className="text-xl sm:text-2xl font-bold text-gray-900">
                            Welcome Back
                        </CardTitle>
                        <CardDescription className="text-sm sm:text-base text-gray-600 px-2">
                            Sign in to access your career roadmaps and continue your professional journey.
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="px-4 sm:px-6">
                        {/* Demo Login Button */}
                        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg animate-slide-up">
                            <div className="text-center">
                                <h3 className="text-sm font-medium text-blue-900 mb-2">Demo Access</h3>
                                <p className="text-xs text-blue-700 mb-3">Try the app without creating an account</p>
                                <Button
                                    onClick={handleDemoLogin}
                                    disabled={loading}
                                    className="w-full bg-blue-600 hover:bg-blue-700"
                                    loading={loading && formData.email === 'demo@example.com'}
                                >
                                    <User className="h-4 w-4 mr-2" />
                                    {loading && formData.email === 'demo@example.com' ? 'Signing In...' : 'Demo Login'}
                                </Button>
                            </div>
                        </div>

                        <div className="relative mb-6">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-300" />
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white text-gray-500">Or continue with your account</span>
                            </div>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6">
                            {errors.general && (
                                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                                    {errors.general}
                                </div>
                            )}

                            <div className="animate-slide-up">
                                <Input
                                    name="email"
                                    type="email"
                                    label="Email Address"
                                    placeholder="Enter your email"
                                    value={formData.email}
                                    onChange={handleInputChange}
                                    error={errors.email}
                                    required
                                    autoComplete="email"
                                />
                            </div>

                            <div className="animate-slide-up animation-delay-200">
                                <Input
                                    name="password"
                                    type="password"
                                    label="Password"
                                    placeholder="Enter your password"
                                    value={formData.password}
                                    onChange={handleInputChange}
                                    error={errors.password}
                                    required
                                    autoComplete="current-password"
                                />
                            </div>

                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0 animate-slide-up animation-delay-400">
                                <div className="flex items-center">
                                    <input
                                        id="remember-me"
                                        name="remember-me"
                                        type="checkbox"
                                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                    />
                                    <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
                                        Remember me
                                    </label>
                                </div>

                                <div className="text-sm">
                                    <Link
                                        to="/forgot-password"
                                        className="font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200"
                                    >
                                        Forgot your password?
                                    </Link>
                                </div>
                            </div>

                            <div className="animate-scale-in animation-delay-600">
                                <Button
                                    type="submit"
                                    loading={loading && formData.email !== 'demo@example.com'}
                                    className="w-full"
                                    disabled={loading}
                                >
                                    <Lock className="h-4 w-4 mr-2" />
                                    {loading && formData.email !== 'demo@example.com' ? 'Signing In...' : 'Sign In'}
                                </Button>
                            </div>
                        </form>

                        <div className="mt-6 animate-fade-in animation-delay-800">
                            <div className="relative">
                                <div className="absolute inset-0 flex items-center">
                                    <div className="w-full border-t border-gray-300" />
                                </div>
                                <div className="relative flex justify-center text-sm">
                                    <span className="px-2 bg-white text-gray-500">New to Career Roadmap?</span>
                                </div>
                            </div>

                            <div className="mt-6">
                                <Link to="/signup">
                                    <Button variant="outline" className="w-full">
                                        Create Your Free Account
                                    </Button>
                                </Link>
                            </div>
                        </div>

                        {/* Trust indicators */}
                        <div className="mt-8 pt-6 border-t border-gray-100">
                            <div className="flex justify-center items-center space-x-6 text-xs text-gray-400">
                                <div className="flex items-center">
                                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                                    Secure Login
                                </div>
                                <div className="flex items-center">
                                    <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                                    Privacy Protected
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}

export default Login
