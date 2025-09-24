import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { API_BASE_URL } from '../config/api'
import {
    Calendar,
    Clock,
    Download,
    Eye,
    Trash2,
    Search,
    Filter,
    Star,
    MoreHorizontal
} from 'lucide-react'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/Card'

const History = () => {
    const { isAuthenticated } = useAuth()
    const [searchTerm, setSearchTerm] = useState('')
    const [filterBy, setFilterBy] = useState('all')
    const [roadmaps, setRoadmaps] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        if (isAuthenticated) {
            fetchRoadmaps()
        }
    }, [isAuthenticated])

    const fetchRoadmaps = async () => {
        try {
            setLoading(true)
            const response = await fetch(`${API_BASE_URL}/roadmaps/history`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            })

            if (response.ok) {
                const data = await response.json()
                setRoadmaps(data.roadmaps || [])
            } else {
                const errorData = await response.json()
                setError(errorData.error || 'Failed to load roadmaps')
            }
        } catch (error) {
            console.error('Error fetching roadmaps:', error)
            setError('Network error. Please check your connection.')
        } finally {
            setLoading(false)
        }
    }

    // Redirect if not authenticated
    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="animate-fade-in">
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">Sign In Required</h1>
                        <p className="text-xl text-gray-600 mb-8">
                            Please sign in to view your roadmap history.
                        </p>
                        <div className="space-x-4">
                            <Link to="/login" className="btn-primary">
                                Sign In
                            </Link>
                            <Link to="/" className="btn-secondary">
                                Back to Home
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        )
    }



    const formatDate = (dateString) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        })
    }



    const filteredRoadmaps = roadmaps.filter(roadmap => {
        const matchesSearch = 
            roadmap.roadmap_summary?.career_goal?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            roadmap.form_data?.interests?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            roadmap.form_data?.careerGoal?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            roadmap.form_data?.currentSkills?.toLowerCase().includes(searchTerm.toLowerCase())

        // For now, just return all matching searches since we don't have status/favorites
        return matchesSearch
    })

    // Show loading state
    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="animate-pulse">
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">Loading...</h1>
                        <p className="text-xl text-gray-600">Fetching your roadmaps...</p>
                    </div>
                </div>
            </div>
        )
    }

    // Show error state
    if (error) {
        return (
            <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <div className="animate-fade-in">
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">Error</h1>
                        <p className="text-xl text-gray-600 mb-8">{error}</p>
                        <Button onClick={fetchRoadmaps}>Try Again</Button>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-12 animate-fade-in">
                    <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
                        Your Career Roadmaps
                    </h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Track your progress, revisit your goals, and continue building your professional future.
                    </p>
                </div>

                {/* Search and Filters */}
                <div className="mb-8 animate-slide-up">
                    <Card>
                        <CardContent className="p-6">
                            <div className="flex flex-col md:flex-row gap-4">
                                <div className="flex-grow">
                                    <div className="relative">
                                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                                        <input
                                            type="text"
                                            placeholder="Search roadmaps by title or skills..."
                                            value={searchTerm}
                                            onChange={(e) => setSearchTerm(e.target.value)}
                                            className="input-field pl-10"
                                        />
                                    </div>
                                </div>

                                <div className="flex items-center space-x-2">
                                    <Filter className="h-4 w-4 text-gray-500" />
                                    <select
                                        value={filterBy}
                                        onChange={(e) => setFilterBy(e.target.value)}
                                        className="input-field min-w-40"
                                    >
                                        <option value="all">All Roadmaps</option>
                                    </select>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8 animate-slide-up animation-delay-200">
                    {[
                        { label: 'Total Roadmaps', value: roadmaps.length, color: 'text-blue-600' },
                        { label: 'Total Skills', value: roadmaps.reduce((sum, r) => sum + (r.roadmap_summary?.total_skills || 0), 0), color: 'text-green-600' },
                        { label: 'Total Phases', value: roadmaps.reduce((sum, r) => sum + (r.roadmap_summary?.total_phases || 0), 0), color: 'text-purple-600' },
                        { label: 'Avg Duration', value: roadmaps.length > 0 ? Math.round(roadmaps.reduce((sum, r) => sum + (r.roadmap_summary?.estimated_weeks || 0), 0) / roadmaps.length) + ' wks' : '0 wks', color: 'text-yellow-600' }
                    ].map((stat, index) => (
                        <Card key={index}>
                            <CardContent className="p-4 text-center">
                                <div className={`text-2xl font-bold ${stat.color} mb-1`}>{stat.value}</div>
                                <div className="text-sm text-gray-600">{stat.label}</div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                {/* Roadmaps Grid */}
                {roadmaps.length === 0 ? (
                    <Card className="animate-fade-in">
                        <CardContent className="p-12 text-center">
                            <div className="text-gray-400 mb-4">
                                <Calendar className="h-12 w-12 mx-auto" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No roadmaps yet</h3>
                            <p className="text-gray-600 mb-6">
                                You haven't generated any career roadmaps yet. Create your first one to get started on your career journey!
                            </p>
                            <Link to="/">
                                <Button>Create Your First Roadmap</Button>
                            </Link>
                        </CardContent>
                    </Card>
                ) : filteredRoadmaps.length === 0 ? (
                    <Card className="animate-fade-in">
                        <CardContent className="p-12 text-center">
                            <div className="text-gray-400 mb-4">
                                <Search className="h-12 w-12 mx-auto" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">No matching roadmaps</h3>
                            <p className="text-gray-600 mb-6">
                                No roadmaps match your search "{searchTerm}". Try different keywords or clear your search.
                            </p>
                            <Button onClick={() => setSearchTerm('')}>Clear Search</Button>
                        </CardContent>
                    </Card>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredRoadmaps.map((roadmap, index) => (
                            <Card
                                key={roadmap.id}
                                className="group hover:shadow-lg transition-all duration-200 animate-scale-in"
                                style={{ animationDelay: `${index * 100 + 400}ms` }}
                            >
                                <CardHeader>
                                    <div className="flex items-start justify-between">
                                        <div className="flex-grow">
                                            <CardTitle className="text-lg mb-2 group-hover:text-blue-600 transition-colors duration-200">
                                                {roadmap.roadmap_summary?.career_goal || 'Career Roadmap'}
                                            </CardTitle>
                                            <CardDescription className="line-clamp-2">
                                                <span className="font-medium">Skills:</span> {roadmap.roadmap_summary?.total_skills || 0} skills • {roadmap.roadmap_summary?.total_phases || 0} phases
                                            </CardDescription>
                                        </div>
                                        <div className="flex items-center space-x-2 ml-2">
                                            <button className="p-1 rounded-md hover:bg-gray-100 transition-colors duration-200">
                                                <MoreHorizontal className="h-4 w-4 text-gray-400" />
                                            </button>
                                        </div>
                                    </div>
                                </CardHeader>

                                <CardContent>
                                    <div className="space-y-4">
                                        {/* Goal */}
                                        {roadmap.form_data?.interests && (
                                            <div>
                                                <p className="text-sm text-gray-600">
                                                    <span className="font-medium">Interests:</span> {roadmap.form_data.interests}
                                                </p>
                                            </div>
                                        )}

                                        {/* Duration */}
                                        <div>
                                            <div className="flex items-center justify-between text-sm mb-1">
                                                <span className="text-gray-600">Estimated Duration</span>
                                                <span className="text-sm font-medium text-blue-600">
                                                    {roadmap.roadmap_summary?.estimated_weeks || 0} weeks
                                                </span>
                                            </div>
                                        </div>

                                        {/* Metadata */}
                                        <div className="flex items-center justify-between text-xs text-gray-500">
                                            <div className="flex items-center space-x-1">
                                                <Calendar className="h-3 w-3" />
                                                <span>{formatDate(roadmap.created_at)}</span>
                                            </div>
                                            <div className="flex items-center space-x-1">
                                                <Clock className="h-3 w-3" />
                                                <span>{roadmap.roadmap_summary?.total_phases || 0} phases</span>
                                            </div>
                                        </div>

                                        {/* Actions */}
                                        <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                className="flex items-center space-x-2"
                                                onClick={() => window.open(`/results?roadmap_id=${roadmap.id}`, '_blank')}
                                            >
                                                <Eye className="h-4 w-4" />
                                                <span>View</span>
                                            </Button>

                                            <div className="flex items-center space-x-2">
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    className="text-gray-600 hover:text-gray-900"
                                                    onClick={() => console.log('Download PDF', roadmap.id)}
                                                >
                                                    <Download className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    className="text-gray-600 hover:text-red-600"
                                                    onClick={() => console.log('Delete roadmap', roadmap.id)}
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}

                {/* Bottom CTA */}
                <div className="text-center mt-16 animate-fade-in animation-delay-800">
                    <div className="card p-8 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">
                            Ready for Your Next Career Move?
                        </h2>
                        <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                            Create a new roadmap to explore different career paths or refine your current goals
                            with updated industry insights.
                        </p>
                        <Link to="/">
                            <Button className="inline-flex items-center space-x-2">
                                <span>Generate New Roadmap</span>
                                <Clock className="h-4 w-4" />
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default History
