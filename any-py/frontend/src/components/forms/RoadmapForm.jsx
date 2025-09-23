import { useState } from 'react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { TextArea } from '../ui/TextArea'
import { Select } from '../ui/Select'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../ui/Card'
import { Sparkles, Target, GraduationCap, Code, Brain } from 'lucide-react'

const RoadmapForm = ({ onSubmit, loading = false }) => {
  const [formData, setFormData] = useState({
    interests: '',
    education: '',
    currentSkills: '',
    careerGoal: ''
  })

  const [errors, setErrors] = useState({})

  const educationLevels = [
    { value: '', label: 'Select your education level' },
    { value: 'high-school', label: 'High School / Secondary' },
    { value: 'associate', label: 'Associate Degree' },
    { value: 'bachelors', label: 'Bachelor\'s Degree' },
    { value: 'masters', label: 'Master\'s Degree' },
    { value: 'phd', label: 'PhD / Doctorate' },
    { value: 'bootcamp', label: 'Bootcamp / Certification' },
    { value: 'self-taught', label: 'Self-Taught' },
    { value: 'other', label: 'Other' }
  ]

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

    if (!formData.interests.trim()) {
      newErrors.interests = 'Please describe your interests'
    }

    if (!formData.education) {
      newErrors.education = 'Please select your education level'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (validateForm()) {
      onSubmit(formData)
    }
  }

  const formSections = [
    {
      icon: Target,
      title: 'Career Interests',
      description: 'What excites you professionally?'
    },
    {
      icon: GraduationCap,
      title: 'Education Background',
      description: 'Your learning foundation'
    },
    {
      icon: Code,
      title: 'Current Skills',
      description: 'What you already know'
    },
    {
      icon: Brain,
      title: 'Career Goals',
      description: 'Where you want to go'
    }
  ]

  return (
    <Card className="max-w-5xl mx-auto animate-fade-in">
      <CardHeader className="text-center pb-6 sm:pb-8 px-4 sm:px-6">
        <div className="flex justify-center mb-4">
          <div className="relative">
            <div className="absolute inset-0 bg-blue-600 rounded-full opacity-10 animate-pulse"></div>
            <Sparkles className="h-10 w-10 sm:h-12 sm:w-12 text-blue-600 relative z-10" />
          </div>
        </div>
        <CardTitle className="text-2xl sm:text-3xl lg:text-4xl text-balance mb-4">
          Design Your Career Journey
        </CardTitle>
        <CardDescription className="text-base sm:text-lg max-w-2xl mx-auto px-4 sm:px-0">
          Share your professional aspirations and let our AI craft a personalized roadmap
          tailored to your unique goals and background.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6 sm:space-y-8 px-4 sm:px-6">
        <form onSubmit={handleSubmit} className="space-y-6 sm:space-y-8">
          {/* Progress indicator */}
          <div className="hidden lg:flex justify-between items-center mb-12">
            {formSections.map((section, index) => {
              const Icon = section.icon
              const isActive =
                (index === 0 && formData.interests) ||
                (index === 1 && formData.education) ||
                (index === 2 && formData.currentSkills) ||
                (index === 3 && formData.careerGoal)

              return (
                <div key={index} className="flex items-center space-x-3">
                  <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-300 ${isActive
                      ? 'border-blue-600 bg-blue-50 text-blue-600'
                      : 'border-gray-300 text-gray-400'
                    }`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="hidden xl:block">
                    <p className={`text-sm font-medium ${isActive ? 'text-gray-900' : 'text-gray-500'}`}>
                      {section.title}
                    </p>
                    <p className="text-xs text-gray-400">{section.description}</p>
                  </div>
                  {index < formSections.length - 1 && (
                    <div className={`w-16 h-0.5 ml-4 ${isActive ? 'bg-blue-200' : 'bg-gray-200'}`} />
                  )}
                </div>
              )
            })}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
            {/* Left Column */}
            <div className="space-y-4 sm:space-y-6">
              <div className="animate-slide-up">
                <TextArea
                  name="interests"
                  label="Career Interests & Passions"
                  placeholder="e.g., Web development, data science, AI/ML, cybersecurity, mobile apps, cloud computing..."
                  value={formData.interests}
                  onChange={handleInputChange}
                  error={errors.interests}
                  required
                  rows={4}
                  helperText="Be specific about what excites you professionally"
                />
              </div>

              <div className="animate-slide-up animation-delay-200">
                <Select
                  name="education"
                  label="Education Level"
                  value={formData.education}
                  onChange={handleInputChange}
                  error={errors.education}
                  required
                >
                  {educationLevels.map(level => (
                    <option key={level.value} value={level.value}>
                      {level.label}
                    </option>
                  ))}
                </Select>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-4 sm:space-y-6">
              <div className="animate-slide-up animation-delay-400">
                <TextArea
                  name="currentSkills"
                  label="Current Skills & Experience"
                  placeholder="e.g., JavaScript, Python, React, SQL, project management, design thinking..."
                  value={formData.currentSkills}
                  onChange={handleInputChange}
                  rows={4}
                  helperText="Include technical skills, tools, and soft skills you've developed"
                />
              </div>

              <div className="animate-slide-up animation-delay-600">
                <TextArea
                  name="careerGoal"
                  label="Career Goals & Aspirations"
                  placeholder="e.g., Become a full-stack developer, transition to data science, start my own tech company..."
                  value={formData.careerGoal}
                  onChange={handleInputChange}
                  rows={4}
                  helperText="Optional: Share your long-term career vision"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-6 sm:pt-8 border-t border-gray-100">
            <div className="flex flex-col items-center text-center space-y-4 sm:space-y-0 sm:flex-row sm:text-left sm:justify-between">
              <div className="flex items-center text-xs sm:text-sm text-gray-500 order-2 sm:order-1">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                <span className="hidden sm:inline">AI-powered analysis • Personalized recommendations</span>
                <span className="sm:hidden">AI-powered • Personalized</span>
              </div>

              <Button
                type="submit"
                loading={loading}
                className="w-full sm:w-auto min-w-48 animate-scale-in animation-delay-600 order-1 sm:order-2"
                disabled={loading}
              >
                <span className="hidden sm:inline">
                  {loading ? 'Generating Your Roadmap...' : 'Generate Career Roadmap'}
                </span>
                <span className="sm:hidden">
                  {loading ? 'Generating...' : 'Generate Roadmap'}
                </span>
              </Button>
            </div>
          </div>
        </form>

        {/* Trust indicators */}
        <div className="pt-8 border-t border-gray-100">
          <div className="flex flex-wrap justify-center items-center gap-8 text-sm text-gray-400">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
              Secure & Private
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              AI-Powered
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
              Personalized
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-orange-500 rounded-full mr-2"></div>
              Export Ready
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default RoadmapForm
