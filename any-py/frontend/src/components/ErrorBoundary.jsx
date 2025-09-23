import { Component } from 'react'

class ErrorBoundary extends Component {
    constructor(props) {
        super(props)
        this.state = { hasError: false }
    }

    static getDerivedStateFromError() {
        return { hasError: true }
    }

    componentDidCatch(error, errorInfo) {
        // You could log this to an error reporting service
        // console.error('ErrorBoundary caught an error', error, errorInfo)
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="min-h-screen flex items-center justify-center p-6">
                    <div className="text-center">
                        <h1 className="text-2xl font-semibold text-gray-900 mb-2">Something went wrong.</h1>
                        <p className="text-gray-600">Please refresh the page or try again.</p>
                    </div>
                </div>
            )
        }
        return this.props.children
    }
}

export default ErrorBoundary


