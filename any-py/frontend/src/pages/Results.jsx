import { useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import {
    Download,
    BookOpen,
    Award,
    Lightbulb,
    Clock,
    CheckCircle2,
    ArrowRight,
    Star,
    ExternalLink
} from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card'

const Results = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()
    const [activeTab, setActiveTab] = useState('skills')
    const [roadmapData, setRoadmapData] = useState(null)
    const [formData, setFormData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const API_BASE_URL = 'http://127.0.0.1:5000/api'
    const roadmapId = searchParams.get('roadmap_id')

    useEffect(() => {
        // Check if we have data from navigation state (fresh generation)
        const stateData = location.state
        if (stateData?.formData && stateData?.roadmap) {
            setFormData(stateData.formData)
            setRoadmapData(stateData.roadmap)
        } 
        // Otherwise, if we have a roadmap ID, fetch it from the API
        else if (roadmapId) {
            fetchRoadmap(roadmapId)
        } 
        // If neither, redirect to home
        else {
            navigate('/')
        }
    }, [roadmapId, location.state, navigate])

    const fetchRoadmap = async (id) => {
        try {
            setLoading(true)
            const response = await fetch(`${API_BASE_URL}/roadmaps/${id}`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            })

            if (response.ok) {
                const data = await response.json()
                setRoadmapData(data.roadmap)
                setFormData(data.form_data || {})
            } else {
                const errorData = await response.json()
                setError(errorData.error || 'Failed to load roadmap')
            }
        } catch (error) {
            console.error('Error fetching roadmap:', error)
            setError('Network error. Please check your connection.')
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-pulse">
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">Loading...</h1>
                        <p className="text-xl text-gray-600">Fetching your roadmap...</p>
                    </div>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">Error</h1>
                    <p className="text-xl text-gray-600 mb-8">{error}</p>
                    <Button onClick={() => navigate('/')}>Back to Home</Button>
                </div>
            </div>
        )
    }

    if (!formData || !roadmapData) {
        return null
    }

    const handleExportPDF = () => {
        // TODO: Implement PDF export functionality
        console.log('Exporting to PDF...')
    }

    const tabs = [
        { id: 'skills', label: 'Skill Path', icon: BookOpen },
        { id: 'platforms', label: 'Platforms', icon: Star },
        { id: 'certifications', label: 'Certifications', icon: Award },
        { id: 'projects', label: 'Projects', icon: Lightbulb },
        { id: 'timeline', label: 'Timeline', icon: Clock }
    ]

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-12 animate-fade-in">
                    <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
                        Your Personalized Career Roadmap
                    </h1>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
                        Based on your interests in <span className="font-semibold text-blue-600">{formData.interests}</span>
                        {formData.careerGoal && (
                            <span> with a goal to <span className="font-semibold text-blue-600">{formData.careerGoal}</span></span>
                        )}
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Button onClick={handleExportPDF} className="inline-flex items-center space-x-2">
                            <Download className="h-4 w-4" />
                            <span>Export to PDF</span>
                        </Button>
                        <Button variant="outline" onClick={() => navigate('/')}>
                            Generate Another Roadmap
                        </Button>
                    </div>
                </div>

                {/* Disclaimer */}
                <div className="card p-4 mb-8 bg-amber-50 border-amber-200 animate-slide-up">
                    <p className="text-sm text-amber-800 text-center">
                        <strong>Disclaimer:</strong> This AI-generated roadmap is a starting point for your career journey.
                        Please research and validate all recommendations before making significant career decisions.
                    </p>
                </div>

                {/* Tab Navigation */}
                <div className="flex flex-wrap justify-center mb-8 animate-slide-up animation-delay-200">
                    <div className="inline-flex bg-white rounded-lg p-1 shadow-sm border border-gray-200">
                        {tabs.map((tab) => {
                            const Icon = tab.icon
                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${activeTab === tab.id
                                            ? 'bg-blue-600 text-white shadow-sm'
                                            : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                                        }`}
                                >
                                    <Icon className="h-4 w-4" />
                                    <span className="hidden sm:inline">{tab.label}</span>
                                </button>
                            )
                        })}
                    </div>
                </div>

                {/* Content Sections */}
                <div className="animate-scale-in animation-delay-400">
                    {activeTab === 'skills' && (
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="flex items-center space-x-2">
                                    <BookOpen className="h-6 w-6 text-blue-600" />
                                    <span>Skill Learning Path</span>
                                </CardTitle>
                                <CardDescription>
                                    A structured progression of skills to master, building from fundamentals to advanced concepts.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-6">
                                    {roadmapData.skill_path?.map((skill, index) => (
                                        <div key={index} className="relative">
                                            {index < roadmapData.skill_path.length - 1 && (
                                                <div className="absolute left-6 top-12 w-0.5 h-16 bg-blue-200"></div>
                                            )}
                                            <div className="flex items-start space-x-4">
                                                <div className="flex-shrink-0 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                                                    {index + 1}
                                                </div>
                                                <div className="flex-grow card-premium p-6">
                                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{skill.name}</h3>
                                                    <p className="text-gray-600 mb-3">{skill.description}</p>
                                                    <div className="flex flex-wrap items-center gap-4 text-sm">
                                                        <div className="flex items-center text-blue-600">
                                                            <Clock className="h-4 w-4 mr-1" />
                                                            <span>{skill.estimated_duration_weeks} weeks</span>
                                                        </div>
                                                        {skill.prerequisites?.length > 0 && (
                                                            <div className="flex items-center text-gray-500">
                                                                <span>Prerequisites: {skill.prerequisites.join(', ')}</span>
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {activeTab === 'platforms' && (
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="flex items-center space-x-2">
                                    <Star className="h-6 w-6 text-blue-600" />
                                    <span>Recommended Learning Platforms</span>
                                </CardTitle>
                                <CardDescription>
                                    Curated platforms and resources to support your learning journey.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {roadmapData.platforms?.map((platform, index) => (
                                        <div key={index} className="card p-6 hover:shadow-lg transition-shadow duration-200">
                                            <h3 className="text-lg font-semibold text-gray-900 mb-2">{platform.name}</h3>
                                            <p className="text-sm text-blue-600 font-medium mb-3">{platform.type}</p>
                                            <p className="text-gray-600 mb-4">{platform.rationale}</p>
                                            <Button variant="outline" size="sm" className="inline-flex items-center space-x-2">
                                                <span>Visit Platform</span>
                                                <ExternalLink className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {activeTab === 'certifications' && (
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="flex items-center space-x-2">
                                    <Award className="h-6 w-6 text-blue-600" />
                                    <span>Relevant Certifications</span>
                                </CardTitle>
                                <CardDescription>
                                    Industry-recognized certifications to validate your expertise and boost your career prospects.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-6">
                                    {roadmapData.certifications?.map((cert, index) => (
                                        <div key={index} className="card p-6 border-l-4 border-l-blue-600">
                                            <div className="flex flex-col md:flex-row md:items-center justify-between mb-3">
                                                <h3 className="text-lg font-semibold text-gray-900">{cert.name}</h3>
                                                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    {cert.level} Level
                                                </span>
                                            </div>
                                            <p className="text-sm text-gray-600 mb-2">Provider: <span className="font-medium">{cert.provider}</span></p>
                                            <p className="text-gray-600">{cert.rationale}</p>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {activeTab === 'projects' && (
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="flex items-center space-x-2">
                                    <Lightbulb className="h-6 w-6 text-blue-600" />
                                    <span>Project Ideas</span>
                                </CardTitle>
                                <CardDescription>
                                    Hands-on projects to build your portfolio and apply your skills in real-world scenarios.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-8">
                                    {['beginner', 'intermediate', 'advanced'].map((level) => (
                                        <div key={level}>
                                            <h3 className="text-xl font-semibold text-gray-900 mb-4 capitalize flex items-center">
                                                <span className={`w-3 h-3 rounded-full mr-2 ${level === 'beginner' ? 'bg-green-500' :
                                                        level === 'intermediate' ? 'bg-yellow-500' : 'bg-red-500'
                                                    }`}></span>
                                                {level} Projects
                                            </h3>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                                {roadmapData.project_ideas?.[level]?.map((project, index) => (
                                                    <div key={index} className="card p-6">
                                                        <h4 className="text-lg font-semibold text-gray-900 mb-3">{project.title}</h4>
                                                        <p className="text-gray-600 mb-4">{project.description}</p>
                                                        <div>
                                                            <p className="text-sm font-medium text-gray-700 mb-2">Learning Objectives:</p>
                                                            <div className="flex flex-wrap gap-2">
                                                                {project.learning_objectives?.map((objective, objIndex) => (
                                                                    <span key={objIndex} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md">
                                                                        {objective}
                                                                    </span>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {activeTab === 'timeline' && (
                        <Card className="mb-8">
                            <CardHeader>
                                <CardTitle className="flex items-center space-x-2">
                                    <Clock className="h-6 w-6 text-blue-600" />
                                    <span>Learning Timeline</span>
                                </CardTitle>
                                <CardDescription>
                                    A realistic timeline with phases and milestones to track your progress.
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-6">
                                    {roadmapData.timeline?.map((phase, index) => (
                                        <div key={index} className="relative">
                                            {index < roadmapData.timeline.length - 1 && (
                                                <div className="absolute left-6 top-16 w-0.5 h-full bg-blue-200"></div>
                                            )}
                                            <div className="flex items-start space-x-4">
                                                <div className="flex-shrink-0 w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                                                    {phase.phase_number}
                                                </div>
                                                <div className="flex-grow card-premium p-6">
                                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{phase.title}</h3>
                                                    <div className="flex items-center text-blue-600 mb-3">
                                                        <Clock className="h-4 w-4 mr-1" />
                                                        <span>{phase.duration_weeks} weeks</span>
                                                    </div>

                                                    <div className="mb-4">
                                                        <p className="text-sm font-medium text-gray-700 mb-2">Focus Skills:</p>
                                                        <div className="flex flex-wrap gap-2">
                                                            {phase.focus_skills?.map((skill, skillIndex) => (
                                                                <span key={skillIndex} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md">
                                                                    {skill}
                                                                </span>
                                                            ))}
                                                        </div>
                                                    </div>

                                                    <div>
                                                        <p className="text-sm font-medium text-gray-700 mb-2">Key Milestones:</p>
                                                        <ul className="space-y-1">
                                                            {phase.milestones?.map((milestone, milestoneIndex) => (
                                                                <li key={milestoneIndex} className="flex items-center text-sm text-gray-600">
                                                                    <CheckCircle2 className="h-4 w-4 text-green-600 mr-2 flex-shrink-0" />
                                                                    {milestone}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* Additional Notes */}
                {roadmapData.notes && roadmapData.notes.length > 0 && (
                    <Card className="mb-8 animate-slide-up animation-delay-600">
                        <CardHeader>
                            <CardTitle>Additional Recommendations</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <ul className="space-y-2">
                                {roadmapData.notes.map((note, index) => (
                                    <li key={index} className="flex items-start">
                                        <ArrowRight className="h-4 w-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                                        <span className="text-gray-600">{note}</span>
                                    </li>
                                ))}
                            </ul>
                        </CardContent>
                    </Card>
                )}

                {/* Bottom CTA */}
                <div className="text-center animate-fade-in animation-delay-800">
                    <p className="text-gray-600 mb-6">
                        Ready to start your journey? Save this roadmap to your account for future reference.
                    </p>
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Button onClick={() => navigate('/signup')} className="inline-flex items-center space-x-2">
                            <span>Create Free Account</span>
                            <ArrowRight className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" onClick={() => navigate('/')}>
                            Generate Another Roadmap
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Results
