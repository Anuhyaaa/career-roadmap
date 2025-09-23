import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card'
import { Sparkles, ArrowLeft, CheckCircle, UserPlus } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Signup = () => {
    const navigate = useNavigate()
    const { register } = useAuth()
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
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

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required'
        }

        if (!formData.email.trim()) {
            newErrors.email = 'Email is required'
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Please enter a valid email'
        }

        if (!formData.password) {
            newErrors.password = 'Password is required'
        } else if (formData.password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters'
        }

        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Passwords do not match'
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!validateForm()) return

        setLoading(true)

        try {
            const result = await register(formData.email, formData.password, formData.name)

            if (result.success) {
                // Navigate to home on success
                navigate('/')
            } else {
                setErrors({ general: result.error })
            }
        } catch (error) {
            setErrors({ general: 'Registration failed. Please try again.' })
        } finally {
            setLoading(false)
        }
    }

    const benefits = [
        'Save unlimited career roadmaps',
        'Track your learning progress',
        'Export roadmaps to PDF',
        'Access premium features',
        'Get personalized recommendations'
    ]

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-6xl mx-auto">
                {/* Back button */}
                <div className="mb-6">
                    <Button
                        variant="ghost"
                        onClick={() => navigate('/')}
                        className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        <span>Back to Home</span>
                    </Button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                    {/* Left side - Benefits */}
                    <div className="animate-fade-in">
                        <div className="text-center lg:text-left mb-8">
                            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
                                Accelerate Your
                                <span className="block text-blue-600">Career Growth</span>
                            </h1>
                            <p className="text-xl text-gray-600 leading-relaxed">
                                Join thousands of professionals who've transformed their careers with our AI-powered roadmaps.
                            </p>
                        </div>

                        <div className="space-y-4 mb-8">
                            {benefits.map((benefit, index) => (
                                <div
                                    key={index}
                                    className="flex items-center space-x-3 animate-slide-up"
                                    style={{ animationDelay: `${index * 100}ms` }}
                                >
                                    <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                                    <span className="text-gray-700">{benefit}</span>
                                </div>
                            ))}
                        </div>

                        <div className="card p-6 bg-blue-50 border-blue-200 animate-slide-up animation-delay-600">
                            <div className="flex items-center space-x-3 mb-3">
                                <div className="flex -space-x-2">
                                    {['JD', 'SM', 'AL', 'RK'].map((initials, index) => (
                                        <div
                                            key={index}
                                            className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-medium border-2 border-white"
                                        >
                                            {initials}
                                        </div>
                                    ))}
                                </div>
                                <div>
                                    <p className="text-sm font-medium text-blue-900">10,000+ professionals</p>
                                    <p className="text-xs text-blue-700">have accelerated their careers</p>
                                </div>
                            </div>
                            <p className="text-sm text-blue-800 italic">
                                "The roadmap was incredibly detailed and helped me land my dream job in just 6 months!"
                            </p>
                        </div>
                    </div>

                    {/* Right side - Form */}
                    <Card className="animate-scale-in animation-delay-300">
                        <CardHeader className="text-center">
                            <div className="flex justify-center mb-4">
                                <div className="relative">
                                    <div className="absolute inset-0 bg-blue-600 rounded-full opacity-10 animate-pulse"></div>
                                    <Sparkles className="h-10 w-10 text-blue-600 relative z-10" />
                                </div>
                            </div>
                            <CardTitle className="text-2xl font-bold text-gray-900">
                                Create Your Account
                            </CardTitle>
                            <CardDescription className="text-gray-600">
                                Start your personalized career journey today. It's free and takes less than a minute.
                            </CardDescription>
                        </CardHeader>

                        <CardContent>
                            <form onSubmit={handleSubmit} className="space-y-6">
                                {errors.general && (
                                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                                        {errors.general}
                                    </div>
                                )}

                                <div className="animate-slide-up">
                                    <Input
                                        name="name"
                                        type="text"
                                        label="Full Name"
                                        placeholder="Enter your full name"
                                        value={formData.name}
                                        onChange={handleInputChange}
                                        error={errors.name}
                                        required
                                        autoComplete="name"
                                    />
                                </div>

                                <div className="animate-slide-up animation-delay-100">
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
                                        placeholder="Create a secure password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        error={errors.password}
                                        required
                                        autoComplete="new-password"
                                        helperText="Must be at least 8 characters long"
                                    />
                                </div>

                                <div className="animate-slide-up animation-delay-300">
                                    <Input
                                        name="confirmPassword"
                                        type="password"
                                        label="Confirm Password"
                                        placeholder="Confirm your password"
                                        value={formData.confirmPassword}
                                        onChange={handleInputChange}
                                        error={errors.confirmPassword}
                                        required
                                        autoComplete="new-password"
                                    />
                                </div>

                                <div className="animate-scale-in animation-delay-500">
                                    <Button
                                        type="submit"
                                        loading={loading}
                                        className="w-full"
                                        disabled={loading}
                                    >
                                        <UserPlus className="h-4 w-4 mr-2" />
                                        {loading ? 'Creating Account...' : 'Create My Free Account'}
                                    </Button>
                                </div>

                                <div className="text-xs text-gray-500 text-center animate-fade-in animation-delay-600">
                                    By signing up, you agree to our{' '}
                                    <Link to="/terms" className="text-blue-600 hover:text-blue-500">
                                        Terms of Service
                                    </Link>{' '}
                                    and{' '}
                                    <Link to="/privacy" className="text-blue-600 hover:text-blue-500">
                                        Privacy Policy
                                    </Link>
                                </div>
                            </form>

                            <div className="mt-6 animate-fade-in animation-delay-700">
                                <div className="relative">
                                    <div className="absolute inset-0 flex items-center">
                                        <div className="w-full border-t border-gray-300" />
                                    </div>
                                    <div className="relative flex justify-center text-sm">
                                        <span className="px-2 bg-white text-gray-500">Already have an account?</span>
                                    </div>
                                </div>

                                <div className="mt-6">
                                    <Link to="/login">
                                        <Button variant="outline" className="w-full">
                                            Sign In to Your Account
                                        </Button>
                                    </Link>
                                </div>
                            </div>

                            {/* Trust indicators */}
                            <div className="mt-8 pt-6 border-t border-gray-100">
                                <div className="flex justify-center items-center space-x-6 text-xs text-gray-400">
                                    <div className="flex items-center">
                                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                                        Free Forever
                                    </div>
                                    <div className="flex items-center">
                                        <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                                        No Credit Card
                                    </div>
                                    <div className="flex items-center">
                                        <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
                                        Secure & Private
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}

export default Signup
