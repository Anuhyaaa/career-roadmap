import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import RoadmapForm from '../components/forms/RoadmapForm'
import { ArrowRight, Star, Users, Zap, CheckCircle, Sparkles } from 'lucide-react'

const Home = () => {
    const navigate = useNavigate()
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const API_BASE_URL = 'http://127.0.0.1:5000/api'
    
    const handleRoadmapSubmit = async (formData) => {
        setLoading(true)
        setError(null)

        try {
            // Call the real backend API
            const response = await fetch(`${API_BASE_URL}/generate-roadmap`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // Important for session cookies
                body: JSON.stringify(formData),
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
            }

            const data = await response.json()

            // Log successful generation for debugging
            console.log('Roadmap generated successfully:', {
                request_id: data.request_id,
                roadmap_id: data.roadmap_id,
                user_authenticated: data.user_authenticated
            })

            // Navigate to results page with real API data
            navigate('/results', {
                state: {
                    formData,
                    roadmap: data.roadmap,
                    roadmapId: data.roadmap_id,
                    saved: data.saved,
                    userAuthenticated: data.user_authenticated
                }
            })
        } catch (error) {
            console.error('Error generating roadmap:', error)
            setError(error.message || 'Failed to generate roadmap. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    const stats = [
        { icon: Users, label: "Professionals Helped", value: "10,000+" },
        { icon: Star, label: "Success Rate", value: "94%" },
        { icon: Zap, label: "Avg. Generation Time", value: "< 30s" },
        { icon: CheckCircle, label: "Career Paths", value: "50+" }
    ]

    const testimonials = [
        {
            name: "Sarah Chen",
            role: "Data Scientist at Google",
            quote: "The roadmap was incredibly detailed and helped me transition from marketing to tech in just 8 months.",
            avatar: "SC"
        },
        {
            name: "Marcus Rodriguez",
            role: "Full-Stack Developer",
            quote: "Finally, a career tool that understands the modern tech landscape. The project suggestions were spot-on.",
            avatar: "MR"
        },
        {
            name: "Emily Watson",
            role: "DevOps Engineer at AWS",
            quote: "The timeline was realistic and the skill progression made perfect sense. Highly recommended!",
            avatar: "EW"
        }
    ]

    return (
        <div className="bg-gradient-to-b from-gray-50 to-white">
            {/* Hero Section */}
            <div className="relative overflow-hidden min-h-screen flex items-center">
                <div className="absolute inset-0 bg-[radial-gradient(45rem_50rem_at_top,theme(colors.blue.100),white)] opacity-20"></div>
                <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
                    <div className="text-center animate-fade-in">
                        <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold text-gray-900 mb-4 sm:mb-6 text-balance">
                            <span className="block">Your Career Journey</span>
                            <span className="block text-blue-600 mt-2">Mapped to Perfection</span>
                        </h1>
                        <p className="text-base sm:text-lg lg:text-xl text-gray-600 max-w-3xl mx-auto mb-6 sm:mb-8 leading-relaxed px-4 sm:px-0">
                            Transform your professional aspirations into a strategic, actionable roadmap.
                            Built with AI precision, designed for ambitious professionals.
                        </p>

                        {/* Quick start CTA */}
                        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8 sm:mb-12">
                            <div className="flex items-center space-x-2 text-xs sm:text-sm text-gray-500">
                                <div className="flex -space-x-2">
                                    {testimonials.slice(0, 3).map((testimonial, index) => (
                                        <div
                                            key={index}
                                            className="w-6 h-6 sm:w-8 sm:h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-medium border-2 border-white"
                                        >
                                            {testimonial.avatar}
                                        </div>
                                    ))}
                                </div>
                                <span className="text-center sm:text-left">Join 10,000+ professionals who've accelerated their careers</span>
                            </div>
                        </div>

                        {/* CTA Button to scroll to form */}
                        <div className="animate-scale-in animation-delay-400 mb-8 sm:mb-12">
                            <button
                                onClick={() => {
                                    const formSection = document.getElementById('design-form')
                                    formSection?.scrollIntoView({ behavior: 'smooth', block: 'start' })
                                }}
                                className="inline-flex items-center space-x-2 px-8 py-4 text-base sm:text-lg font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-105"
                            >
                                <Sparkles className="h-5 w-5" />
                                <span>Start Your Journey</span>
                                <ArrowRight className="h-5 w-5" />
                            </button>
                        </div>
                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 lg:gap-8 mt-12 sm:mt-16 animate-slide-up animation-delay-200">
                        {stats.map((stat, index) => {
                            const Icon = stat.icon
                            return (
                                <div key={index} className="text-center">
                                    <div className="flex justify-center mb-1 sm:mb-2">
                                        <Icon className="h-6 w-6 sm:h-7 sm:w-7 lg:h-8 lg:w-8 text-blue-600" />
                                    </div>
                                    <div className="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900">{stat.value}</div>
                                    <div className="text-xs sm:text-sm text-gray-600">{stat.label}</div>
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>

            {/* Main Form Section */}
            <div id="design-form" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <div className="flex">
                            <div className="ml-3">
                                <h3 className="text-sm font-medium text-red-800">
                                    Error generating roadmap
                                </h3>
                                <div className="mt-2 text-sm text-red-700">
                                    <p>{error}</p>
                                </div>
                                <div className="mt-4">
                                    <button
                                        type="button"
                                        className="bg-red-100 px-2 py-1.5 rounded-md text-sm font-medium text-red-800 hover:bg-red-200"
                                        onClick={() => setError(null)}
                                    >
                                        Dismiss
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                <RoadmapForm onSubmit={handleRoadmapSubmit} loading={loading} />
            </div>

            {/* Features Section */}
            <div className="bg-white py-16 sm:py-20 lg:py-24">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12 sm:mb-16">
                        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                            Precision-Engineered for Success
                        </h2>
                        <p className="text-base sm:text-lg text-gray-600 max-w-2xl mx-auto px-4 sm:px-0">
                            Every detail matters when crafting your professional future.
                            Our platform delivers Swiss-level precision in career planning.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
                        {[
                            {
                                title: "AI-Driven Analysis",
                                description: "Advanced algorithms analyze industry trends, skill demands, and career trajectories to provide personalized recommendations.",
                                icon: "🧠"
                            },
                            {
                                title: "Actionable Timelines",
                                description: "Realistic, milestone-based timelines that adapt to your pace and circumstances, not generic advice.",
                                icon: "⏱️"
                            },
                            {
                                title: "Industry Validated",
                                description: "Recommendations backed by real industry data and validated by professionals at leading tech companies.",
                                icon: "✅"
                            }
                        ].map((feature, index) => (
                            <div
                                key={index}
                                className="card p-8 text-center animate-slide-up"
                                style={{ animationDelay: `${index * 200 + 400}ms` }}
                            >
                                <div className="text-4xl mb-4">{feature.icon}</div>
                                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                                <p className="text-gray-600">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Testimonials */}
            <div className="bg-gray-50 py-24">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                            Trusted by Industry Leaders
                        </h2>
                        <p className="text-lg text-gray-600">
                            Real results from real professionals who transformed their careers.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {testimonials.map((testimonial, index) => (
                            <div
                                key={index}
                                className="card p-6 animate-scale-in"
                                style={{ animationDelay: `${index * 200 + 600}ms` }}
                            >
                                <p className="text-gray-600 mb-4 italic">"{testimonial.quote}"</p>
                                <div className="flex items-center">
                                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-medium mr-3">
                                        {testimonial.avatar}
                                    </div>
                                    <div>
                                        <div className="font-semibold text-gray-900">{testimonial.name}</div>
                                        <div className="text-sm text-gray-600">{testimonial.role}</div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* CTA Section */}
            <div className="bg-gray-900 py-16">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
                        Ready to Design Your Future?
                    </h2>
                    <p className="text-xl text-gray-300 mb-8">
                        Join thousands of professionals who've already accelerated their careers.
                    </p>
                    <button
                        onClick={() => {
                            const formSection = document.getElementById('design-form')
                            formSection?.scrollIntoView({ behavior: 'smooth', block: 'start' })
                        }}
                        className="btn-primary bg-blue-600 hover:bg-blue-700 text-white inline-flex items-center space-x-2 text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4"
                    >
                        <span>Start Your Journey</span>
                        <ArrowRight className="h-4 w-4 sm:h-5 sm:w-5" />
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Home
