"""
Main Application - Career Roadmap Generator Backend
Combines all modules and initializes the Flask application
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import json
import uuid
import traceback
from google import genai
from google.genai import types
from typing import Dict, Any, Optional
import traceback
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from auth import auth_bp, init_auth_db
from roadmap_routes import roadmap_bp, init_roadmap_db
from pdf_service import pdf_bp, init_pdf_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2024')

# Session configuration for development
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Keep this True for security
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Allow cross-origin requests in development
app.config['SESSION_COOKIE_DOMAIN'] = None  # Let Flask handle domain automatically

# Enable CORS for frontend
allowed_origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
CORS(app, 
     origins=allowed_origins, 
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# MongoDB connection
MONGO_URI = os.environ.get('MONGO_URI', "mongodb+srv://anuhya:anuhya123@cluster0.1yxhld9.mongodb.net/career?retryWrites=true&w=majority&appName=Cluster0")

try:
    mongo_client = MongoClient(MONGO_URI)
    # Test connection
    mongo_client.admin.command('ping')
    db = mongo_client.career
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Collections
users_collection = db.users
roadmap_requests_collection = db.roadmap_requests
roadmaps_collection = db.roadmaps

# Test connection function
def test_connection():
    """Test MongoDB connection"""
    try:
        mongo_client.admin.command('ping')
        logger.info("MongoDB connection test successful")
        return True
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {str(e)}")
        return False

# Request logging middleware for debugging
@app.before_request
def log_request_info():
    logger.info(f'Request: {request.method} {request.url}')
    logger.info(f'Headers: {dict(request.headers)}')
    logger.info(f'Session: {dict(session)}')

# Initialize database connections for blueprints
init_auth_db(db)
init_roadmap_db(db)
init_pdf_db(db)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(roadmap_bp)
app.register_blueprint(pdf_bp)

# Google Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. AI generation will fail.")
    gemini_client = None
else:
    # The client gets the API key from the environment variable `GEMINI_API_KEY`.
    # This is the correct way to initialize, assuming the env var is set.
    gemini_client = genai.Client()

# Helper functions
def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == '_id' and isinstance(value, ObjectId):
                result['id'] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                result[key] = serialize_mongo_doc(value)
            else:
                result[key] = value
        return result
    return doc

def get_current_user():
    """Get current authenticated user from session"""
    try:
        if 'user_id' not in session:
            return None
        
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            return serialize_mongo_doc(user)
        return None
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return None

# AI Service Functions
def construct_ai_prompt(form_data: Dict[str, Any]) -> str:
    """Construct the comprehensive prompt for Gemini 2.5 Flash AI model"""
    
    interests = form_data.get('interests', 'technology')
    education = form_data.get('education', 'General education')
    current_skills = form_data.get('currentSkills', 'Basic skills')
    career_goal = form_data.get('careerGoal', 'Career advancement')
    experience_level = form_data.get('experienceLevel', 'Beginner')
    time_commitment = form_data.get('timeCommitment', '10 hours per week')
    
    prompt = f"""Create a comprehensive career roadmap for someone with the following profile:

Interests: {interests}
Education: {education}
Current Skills: {current_skills}
Career Goal: {career_goal}
Experience Level: {experience_level}
Time Commitment: {time_commitment}

Please provide ONLY a valid JSON response with this exact structure:

{{
  "skill_path": [
    {{
      "name": "skill name",
      "description": "description of the skill",
      "prerequisites": ["prerequisite skills"],
      "estimated_duration_weeks": 4
    }}
  ],
  "platforms": [
    {{
      "name": "platform name",
      "type": "platform type",
      "rationale": "why this platform"
    }}
  ],
  "certifications": [
    {{
      "name": "certification name",
      "provider": "provider name",
      "level": "Beginner",
      "rationale": "why valuable"
    }}
  ],
  "project_ideas": {{
    "beginner": [
      {{
        "title": "project title",
        "description": "project description",
        "learning_objectives": ["what you'll learn"]
      }}
    ],
    "intermediate": [
      {{
        "title": "project title",
        "description": "project description",
        "learning_objectives": ["what you'll learn"]
      }}
    ],
    "advanced": [
      {{
        "title": "project title",
        "description": "project description",
        "learning_objectives": ["what you'll learn"]
      }}
    ]
  }},
  "timeline": [
    {{
      "phase_number": 1,
      "title": "phase title",
      "duration_weeks": 8,
      "focus_skills": ["skills to focus on"],
      "milestones": ["milestones to achieve"]
    }}
  ],
  "notes": ["career advice and tips"]
}}

Important: Return ONLY the JSON object, no markdown formatting or additional text."""
    
    return prompt

def validate_and_enhance_roadmap(roadmap_data: Dict[str, Any], form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and enhance the roadmap data with fallbacks if needed"""
    
    # Define fallback data based on form input
    interests = form_data.get('interests', 'technology')
    career_goal = form_data.get('careerGoal', 'professional development')
    
    # Ensure all required fields exist with fallbacks
    if 'skill_path' not in roadmap_data or not roadmap_data['skill_path']:
        roadmap_data['skill_path'] = [
            {
                "name": "Foundation Skills",
                "description": f"Build fundamental skills in {interests}",
                "prerequisites": [],
                "estimated_duration_weeks": 4
            },
            {
                "name": "Intermediate Concepts",
                "description": f"Develop intermediate knowledge in {interests}",
                "prerequisites": ["Foundation Skills"],
                "estimated_duration_weeks": 6
            }
        ]
    
    if 'platforms' not in roadmap_data or not roadmap_data['platforms']:
        roadmap_data['platforms'] = [
            {
                "name": "Coursera",
                "type": "Online Learning Platform",
                "rationale": "Offers university-level courses with certificates"
            },
            {
                "name": "YouTube",
                "type": "Free Video Platform",
                "rationale": "Free tutorials and practical demonstrations"
            }
        ]
    
    if 'certifications' not in roadmap_data or not roadmap_data['certifications']:
        roadmap_data['certifications'] = [
            {
                "name": "Professional Certificate",
                "provider": "Industry Leaders",
                "level": "Intermediate",
                "rationale": f"Validates expertise in {interests}"
            }
        ]
    
    if 'project_ideas' not in roadmap_data or not roadmap_data['project_ideas']:
        roadmap_data['project_ideas'] = {
            "beginner": [
                {
                    "title": "Basic Portfolio Project",
                    "description": f"Create a simple project showcasing {interests} skills",
                    "learning_objectives": ["Practical application", "Portfolio building"]
                }
            ],
            "intermediate": [
                {
                    "title": "Intermediate Application",
                    "description": f"Build a more complex application in {interests}",
                    "learning_objectives": ["Advanced concepts", "Problem solving"]
                }
            ],
            "advanced": [
                {
                    "title": "Advanced Capstone Project",
                    "description": f"Comprehensive project demonstrating mastery of {interests}",
                    "learning_objectives": ["System design", "Best practices"]
                }
            ]
        }
    
    if 'timeline' not in roadmap_data or not roadmap_data['timeline']:
        roadmap_data['timeline'] = [
            {
                "phase_number": 1,
                "title": "Foundation Phase",
                "duration_weeks": 8,
                "focus_skills": ["Fundamentals"],
                "milestones": ["Complete basic concepts", "Build first project"]
            },
            {
                "phase_number": 2,
                "title": "Development Phase",
                "duration_weeks": 12,
                "focus_skills": ["Advanced concepts"],
                "milestones": ["Master intermediate skills", "Create portfolio"]
            }
        ]
    
    if 'notes' not in roadmap_data or not roadmap_data['notes']:
        roadmap_data['notes'] = [
            "Stay consistent with your learning schedule",
            "Build projects to reinforce theoretical knowledge",
            "Join relevant communities and network with professionals",
            "Keep your skills updated with industry trends",
            f"Focus on practical applications of {interests} in real-world scenarios"
        ]
    
    # Validate data integrity
    for field in ['skill_path', 'platforms', 'certifications', 'timeline']:
        if not isinstance(roadmap_data.get(field), list):
            logger.warning(f"Field {field} is not a list, converting")
            roadmap_data[field] = []
    
    # Ensure project_ideas has the correct structure
    if not isinstance(roadmap_data.get('project_ideas'), dict):
        roadmap_data['project_ideas'] = {"beginner": [], "intermediate": [], "advanced": []}
    else:
        for level in ['beginner', 'intermediate', 'advanced']:
            if level not in roadmap_data['project_ideas'] or not isinstance(roadmap_data['project_ideas'][level], list):
                roadmap_data['project_ideas'][level] = []
    
    logger.info(f"Roadmap validation complete. Fields: {list(roadmap_data.keys())}")
    return roadmap_data

def generate_roadmap_with_ai(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate career roadmap using Google Gemini 2.5 Flash AI"""
    try:
        if not gemini_client:
            raise Exception("Gemini client is not initialized. Check API key.")

        prompt = construct_ai_prompt(form_data)
        
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                candidate_count=1,
                max_output_tokens=8000,
                stop_sequences=["```", "---", "END_ROADMAP"]
            )
        )
        
        if not response.text:
            raise Exception("Empty response from AI model")
        
        response_text = response.text.strip()
        
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        try:
            roadmap_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception("Invalid JSON response from AI model")
        
        roadmap_data = validate_and_enhance_roadmap(roadmap_data, form_data)
        
        return roadmap_data
        
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        mongo_client.admin.command('ping')
        db_status = 'connected'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'version': '1.0.0'
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
        user_id = current_user['id'] if current_user else None
        
        logger.info(f"Current user: {current_user}")
        logger.info(f"Session: {dict(session)}")
        logger.info(f"User ID: {user_id}")
        
        # Save request to database
        request_doc = {
            'request_id': request_id,
            'user_id': ObjectId(user_id) if user_id else None,
            'form_data': data,
            'created_at': datetime.utcnow(),
            'status': 'processing'
        }
        
        roadmap_requests_collection.insert_one(request_doc)
        
        try:
            # Generate roadmap using AI
            logger.info(f"Generating roadmap for request {request_id}")
            roadmap_data = generate_roadmap_with_ai(data)
            
            # Save roadmap to database
            roadmap_doc = {
                'request_id': request_id,
                'user_id': ObjectId(user_id) if user_id else None,
                'roadmap_data': roadmap_data,
                'created_at': datetime.utcnow()
            }
            
            result = roadmaps_collection.insert_one(roadmap_doc)
            
            # Update request status
            roadmap_requests_collection.update_one(
                {'request_id': request_id},
                {'$set': {'status': 'completed', 'completed_at': datetime.utcnow()}}
            )
            
            # Return the generated roadmap
            response_data = {
                'request_id': request_id,
                'roadmap_id': str(result.inserted_id),
                'roadmap': roadmap_data,
                'user_authenticated': current_user is not None,
                'saved': current_user is not None
            }
            
            logger.info(f"Successfully generated roadmap for request {request_id}")
            return jsonify(response_data)
            
        except Exception as e:
            # Update request status to failed
            roadmap_requests_collection.update_one(
                {'request_id': request_id},
                {'$set': {'status': 'failed', 'error': str(e), 'failed_at': datetime.utcnow()}}
            )
            raise
        
    except Exception as e:
        logger.error(f"Error generating roadmap: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to generate roadmap',
            'details': str(e)
        }), 500

# Helper functions for MongoDB
def get_current_user():
    """Get current user from session"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return None
        
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['id'] = str(user['_id'])
            user.pop('_id', None)
        
        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        return None



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

if __name__ == '__main__':
    if not test_connection():
        logger.critical("Cannot start server - database connection failed")
        exit(1)
    
    logger.info("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)