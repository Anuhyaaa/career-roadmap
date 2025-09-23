"""
Simple server test to verify the basic API functionality
"""

from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Career Roadmap Generator API is running',
        'version': '1.0.0'
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        'message': 'API is working correctly',
        'endpoints': [
            'GET /api/health',
            'POST /api/generate-roadmap',
            'POST /api/auth/register',
            'POST /api/auth/login',
            'GET /api/roadmaps/history'
        ]
    })

if __name__ == '__main__':
    print("Starting Career Roadmap Generator API...")
    print("API will be available at: http://localhost:5000")
    print("\nAvailable endpoints:")
    print("- GET  /api/health")
    print("- GET  /api/test")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)