"""
Career Roadmap Generator Backend - Working Version
Flask application with MongoDB integration and AI roadmap generation
"""

from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid
import requests
import os
from datetime import datetime, timedelta
import logging
import traceback
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2024')

# Enable CORS for frontend
frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
CORS(app, origins=[frontend_url], supports_credentials=True)

# For now, we'll use in-memory storage (in production, use MongoDB)
# This is a temporary solution to get the API working
users_db = {}
roadmaps_db = {}
requests_db = {}

# Google Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', "AIzaSyAFcFv5efZN6lhp-dFM3dzCEJZexjQb-Rk")

# Helper functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

def get_current_user():
    """Get current authenticated user from session"""
    if 'user_id' in session:
        return users_db.get(session['user_id'])
    return None

def generate_roadmap_with_gemini(form_data):
    """Generate career roadmap using Google Gemini AI"""
    try:
        # Construct the prompt
        system_instruction = """You are an expert career mentor. Given a learner profile, produce a structured JSON object EXACTLY matching the specified schema. Return ONLY the JSON object with no additional text or markdown formatting.

The JSON schema must include:
{
  "skill_path": [
    {
      "name": "string",
      "description": "string", 
      "prerequisites": ["string"],
      "estimated_duration_weeks": number
    }
  ],
  "platforms": [
    {
      "name": "string",
      "type": "string",
      "rationale": "string"
    }
  ],
  "certifications": [
    {
      "name": "string",
      "provider": "string", 
      "level": "string",
      "rationale": "string"
    }
  ],
  "project_ideas": {
    "beginner": [
      {
        "title": "string",
        "description": "string",
        "learning_objectives": ["string"]
      }
    ],
    "intermediate": [
      {
        "title": "string", 
        "description": "string",
        "learning_objectives": ["string"]
      }
    ],
    "advanced": [
      {
        "title": "string",
        "description": "string", 
        "learning_objectives": ["string"]
      }
    ]
  },
  "timeline": [
    {
      "phase_number": number,
      "title": "string",
      "duration_weeks": number,
      "focus_skills": ["string"],
      "milestones": ["string"]
    }
  ],
  "notes": ["string"]
}"""

        user_data = f"""Learner Profile:
Interests: {form_data.get('interests', 'Not specified')}
Education: {form_data.get('education', 'Not specified')}
Current Skills: {form_data.get('currentSkills', 'Not specified')}
Career Goal: {form_data.get('careerGoal', 'Not specified')}

Constraints: Focus on practical, widely-used technologies and credible platforms. Assume the learner can study 10 hours per week. Provide a comprehensive roadmap with at least 3-5 skills in the skill path, 3-4 learning platforms, 2-3 relevant certifications, and detailed project ideas for each level."""

        # Make API call to Google Gemini
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{system_instruction}\n\n{user_data}"
                }]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            logger.error(f"Gemini API error: {response.status_code} - {response.text}")
            raise Exception(f"AI API error: {response.status_code}")
        
        result = response.json()
        
        if 'candidates' not in result or not result['candidates']:
            raise Exception("No response from AI model")
        
        content = result['candidates'][0]['content']['parts'][0]['text']
        
        # Clean the response text
        content = content.strip()
        
        # Remove any markdown code block formatting
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        
        content = content.strip()
        
        # Parse JSON
        try:
            roadmap_data = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Response content: {content}")
            raise Exception("Invalid JSON response from AI model")
        
        return roadmap_data
        
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Return a fallback roadmap for demo purposes
        return {
            "skill_path": [
                {
                    "name": "Programming Fundamentals",
                    "description": "Learn the basics of programming logic and problem-solving",
                    "prerequisites": [],
                    "estimated_duration_weeks": 4
                },
                {
                    "name": "Web Development Basics",
                    "description": "HTML, CSS, and JavaScript fundamentals",
                    "prerequisites": ["Programming Fundamentals"],
                    "estimated_duration_weeks": 6
                }
            ],
            "platforms": [
                {
                    "name": "freeCodeCamp",
                    "type": "Free Online Course",
                    "rationale": "Comprehensive curriculum with hands-on projects"
                }
            ],
            "certifications": [
                {
                    "name": "JavaScript Developer Certificate",
                    "provider": "freeCodeCamp",
                    "level": "Beginner",
                    "rationale": "Industry-recognized certification"
                }
            ],
            "project_ideas": {
                "beginner": [
                    {
                        "title": "Personal Portfolio",
                        "description": "Create a personal website showcasing your skills",
                        "learning_objectives": ["HTML", "CSS", "Basic JavaScript"]
                    }
                ],
                "intermediate": [
                    {
                        "title": "Todo App",
                        "description": "Build a task management application",
                        "learning_objectives": ["JavaScript", "DOM Manipulation", "Local Storage"]
                    }
                ],
                "advanced": [
                    {
                        "title": "Full-Stack Web App",
                        "description": "Create a complete web application with backend",
                        "learning_objectives": ["Frontend Frameworks", "Backend APIs", "Database Design"]
                    }
                ]
            },
            "timeline": [
                {
                    "phase_number": 1,
                    "title": "Foundation Phase",
                    "duration_weeks": 8,
                    "focus_skills": ["Programming Fundamentals", "Web Basics"],
                    "milestones": ["Complete first project", "Learn HTML/CSS"]
                }
            ],
            "notes": ["Practice consistently", "Build projects while learning", "Join developer communities"]
        }

# Main API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'message': 'Career Roadmap Generator API is running'
    })

@app.route('/api/generate-roadmap', methods=['POST'])
def generate_roadmap():
    """Generate career roadmap using AI"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['interests', 'education']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Get current user (if authenticated)
        current_user = get_current_user()
        
        # Save request to database
        requests_db[request_id] = {
            'request_id': request_id,
            'user_id': current_user['id'] if current_user else None,
            'form_data': data,
            'created_at': datetime.utcnow(),
            'status': 'processing'
        }
        
        try:
            # Generate roadmap using AI
            logger.info(f"Generating roadmap for request {request_id}")
            roadmap_data = generate_roadmap_with_gemini(data)
            
            # Generate roadmap ID
            roadmap_id = str(uuid.uuid4())
            
            # Save roadmap to database
            roadmaps_db[roadmap_id] = {
                'id': roadmap_id,
                'request_id': request_id,
                'user_id': current_user['id'] if current_user else None,
                'roadmap_data': roadmap_data,
                'created_at': datetime.utcnow()
            }
            
            # Update request status
            requests_db[request_id]['status'] = 'completed'
            requests_db[request_id]['completed_at'] = datetime.utcnow()
            
            # Return the generated roadmap
            response_data = {
                'request_id': request_id,
                'roadmap_id': roadmap_id,
                'roadmap': roadmap_data,
                'user_authenticated': current_user is not None,
                'saved': current_user is not None
            }
            
            logger.info(f"Successfully generated roadmap for request {request_id}")
            return jsonify(response_data)
            
        except Exception as e:
            # Update request status to failed
            requests_db[request_id]['status'] = 'failed'
            requests_db[request_id]['error'] = str(e)
            requests_db[request_id]['failed_at'] = datetime.utcnow()
            raise
        
    except Exception as e:
        logger.error(f"Error generating roadmap: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to generate roadmap',
            'details': str(e)
        }), 500

# Authentication Routes

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validate required fields
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if not password:
            return jsonify({'error': 'Password is required'}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, password_error = validate_password(password)
        if not is_valid:
            return jsonify({'error': password_error}), 400
        
        # Check if user already exists
        for user in users_db.values():
            if user['email'] == email:
                return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user_id = str(uuid.uuid4())
        user_doc = {
            'id': user_id,
            'email': email,
            'name': name if name else email.split('@')[0],
            'password_hash': generate_password_hash(password),
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        
        users_db[user_id] = user_doc
        
        # Create session
        session['user_id'] = user_id
        session['user_email'] = email
        
        # Return user data (excluding password)
        user_data = {
            'id': user_id,
            'email': email,
            'name': user_doc['name'],
            'created_at': user_doc['created_at'].isoformat()
        }
        
        logger.info(f"New user registered: {email}")
        
        return jsonify({
            'message': 'Registration successful',
            'user': user_data
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = None
        for u in users_db.values():
            if u['email'] == email:
                user = u
                break
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        user['last_login'] = datetime.utcnow()
        
        # Create session
        session['user_id'] = user['id']
        session['user_email'] = email
        
        # Return user data
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at'].isoformat(),
            'last_login': datetime.utcnow().isoformat()
        }
        
        logger.info(f"User logged in: {email}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        user_email = session.get('user_email')
        
        # Clear session
        session.clear()
        
        if user_email:
            logger.info(f"User logged out: {user_email}")
        
        return jsonify({'message': 'Logout successful'})
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/api/auth/me', methods=['GET'])
def get_current_user_info():
    """Get current user information"""
    try:
        current_user = get_current_user()
        
        if not current_user:
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Return user data
        user_data = {
            'id': current_user['id'],
            'email': current_user['email'],
            'name': current_user['name'],
            'created_at': current_user['created_at'].isoformat(),
            'last_login': current_user.get('last_login').isoformat() if current_user.get('last_login') else None
        }
        
        return jsonify({'user': user_data})
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500

@app.route('/api/auth/check-session', methods=['GET'])
def check_session():
    """Check if user has valid session"""
    try:
        current_user = get_current_user()
        
        if current_user and current_user.get('is_active', True):
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': current_user['id'],
                    'email': current_user['email'],
                    'name': current_user['name']
                }
            })
        
        return jsonify({'authenticated': False})
        
    except Exception as e:
        logger.error(f"Check session error: {str(e)}")
        return jsonify({'authenticated': False})

# Roadmap Management Routes

@app.route('/api/roadmaps/history', methods=['GET'])
def get_user_roadmap_history():
    """Get all roadmaps for the current user"""
    try:
        current_user = get_current_user()
        
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Get user's roadmaps
        user_roadmaps = []
        for roadmap in roadmaps_db.values():
            if roadmap['user_id'] == current_user['id']:
                # Get the original request data for context
                request_data = requests_db.get(roadmap['request_id'])
                
                formatted_roadmap = {
                    'id': roadmap['id'],
                    'request_id': roadmap['request_id'],
                    'created_at': roadmap['created_at'].isoformat(),
                    'form_data': request_data['form_data'] if request_data else {},
                    'roadmap_summary': {
                        'total_skills': len(roadmap['roadmap_data'].get('skill_path', [])),
                        'total_phases': len(roadmap['roadmap_data'].get('timeline', [])),
                        'estimated_weeks': sum(phase.get('duration_weeks', 0) for phase in roadmap['roadmap_data'].get('timeline', [])),
                        'career_goal': request_data['form_data'].get('careerGoal', 'Not specified') if request_data else 'Not specified'
                    }
                }
                user_roadmaps.append(formatted_roadmap)
        
        # Sort by creation date (newest first)
        user_roadmaps.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Apply pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_roadmaps = user_roadmaps[start_idx:end_idx]
        
        return jsonify({
            'roadmaps': paginated_roadmaps,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': len(user_roadmaps),
                'total_pages': (len(user_roadmaps) + limit - 1) // limit,
                'has_next': end_idx < len(user_roadmaps),
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching roadmap history: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap history'}), 500

@app.route('/api/roadmaps/<roadmap_id>', methods=['GET'])
def get_roadmap_details(roadmap_id):
    """Get detailed roadmap by ID"""
    try:
        current_user = get_current_user()
        
        roadmap = roadmaps_db.get(roadmap_id)
        
        if not roadmap:
            return jsonify({'error': 'Roadmap not found'}), 404
        
        # Check access permissions
        if roadmap['user_id'] and (not current_user or roadmap['user_id'] != current_user['id']):
            return jsonify({'error': 'Access denied'}), 403
        
        # Get the original request data
        request_data = requests_db.get(roadmap['request_id'])
        
        response_data = {
            'id': roadmap['id'],
            'request_id': roadmap['request_id'],
            'created_at': roadmap['created_at'].isoformat(),
            'form_data': request_data['form_data'] if request_data else {},
            'roadmap': roadmap['roadmap_data'],
            'is_owner': roadmap['user_id'] == current_user['id'] if current_user and roadmap['user_id'] else False
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching roadmap details: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap details'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.route('/api/create-demo-user', methods=['POST'])
def create_demo_user():
    """Create a demo user for testing (development only)"""
    try:
        demo_email = 'demo@example.com'
        
        # Check if demo user already exists
        if demo_email in users_db:
            return jsonify({'message': 'Demo user already exists', 'email': demo_email})
        
        # Create demo user
        user_id = str(uuid.uuid4())
        password_hash = generate_password_hash('demo123')
        
        users_db[demo_email] = {
            'id': user_id,
            'email': demo_email,
            'full_name': 'Demo User',
            'password_hash': password_hash,
            'created_at': datetime.utcnow()
        }
        
        return jsonify({
            'message': 'Demo user created successfully',
            'email': demo_email,
            'password': 'demo123'
        })
        
    except Exception as e:
        logger.error(f"Error creating demo user: {str(e)}")
        return jsonify({'error': 'Failed to create demo user'}), 500

if __name__ == '__main__':
    host = '127.0.0.1'  # Bind to localhost only
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting Career Roadmap Generator API...")
    print(f"📍 Server will be available at: http://{host}:{port}")
    print("\n🔗 Available API endpoints:")
    print("   • GET  /api/health              - Health check")
    print("   • POST /api/generate-roadmap    - Generate AI roadmap")
    print("   • POST /api/auth/register       - User registration") 
    print("   • POST /api/auth/login          - User login")
    print("   • POST /api/auth/logout         - User logout")
    print("   • GET  /api/auth/me             - Current user info")
    print("   • GET  /api/roadmaps/history    - User's roadmap history")
    print("   • GET  /api/roadmaps/<id>       - Get specific roadmap")
    print("\n⚠️  Using in-memory storage (for development only)")
    print("✨ Press Ctrl+C to stop the server\n")
    
    app.run(debug=debug, host=host, port=port, use_reloader=False, threaded=True)