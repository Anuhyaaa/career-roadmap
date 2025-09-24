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
app.config['SESSION_COOKIE_SECURE'] = False  # Must be False for HTTP (development)
app.config['SESSION_COOKIE_HTTPONLY'] = False  # Set to False to allow JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Lax allows some cross-origin requests
app.config['SESSION_COOKIE_DOMAIN'] = None  # Let Flask handle domain automatically
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Session expires in 24 hours

# Enable CORS for frontend
allowed_origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5174',
    'https://*.vercel.app',  # Allow all Vercel deployments
    os.environ.get('FRONTEND_URL', 'http://localhost:5173')  # Allow custom frontend URL
]
CORS(app, 
     origins=allowed_origins, 
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization', 'Cookie'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     expose_headers=['Set-Cookie'])

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

# Root route for health check
@app.route('/')
def home():
    """Root endpoint for health check"""
    return jsonify({
        'message': 'Career Roadmap Generator API',
        'status': 'running',
        'version': '1.0.0'
    })

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if test_connection() else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    })

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

def generate_roadmap_with_ai(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate career roadmap using Google Gemini AI"""
    try:
        prompt = construct_ai_prompt(form_data)
        
        # Generate content using Gemini
        response = gemini_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        
        if not response.text:
            raise Exception("Empty response from AI model")
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove any markdown code block formatting
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            roadmap_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            logger.error(f"Response text: {response_text}")
            raise Exception("Invalid JSON response from AI model")
        
        # Validate required fields
        required_fields = ['skill_path', 'platforms', 'certifications', 'project_ideas', 'timeline', 'notes']
        for field in required_fields:
            if field not in roadmap_data:
                logger.warning(f"Missing field {field} in AI response")
        
        return roadmap_data
        
    except Exception as e:
        logger.error(f"AI generation error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

# Main roadmap generation endpoint
@app.route('/api/generate-roadmap', methods=['POST'])
def generate_roadmap():
    """Generate a career roadmap based on user input"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['interests', 'careerGoal']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Get current user if authenticated
        current_user = get_current_user()
        user_id = ObjectId(current_user['id']) if current_user else None
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Store the request
        request_doc = {
            'request_id': request_id,
            'user_id': user_id,
            'form_data': data,
            'created_at': datetime.utcnow(),
            'status': 'processing'
        }
        
        roadmap_requests_collection.insert_one(request_doc)
        
        # Generate roadmap with AI
        roadmap_data = generate_roadmap_with_ai(data)
        
        # Store the generated roadmap
        roadmap_doc = {
            'request_id': request_id,
            'user_id': user_id,
            'roadmap_data': roadmap_data,
            'created_at': datetime.utcnow()
        }
        
        result = roadmaps_collection.insert_one(roadmap_doc)
        roadmap_id = str(result.inserted_id)
        
        # Update request status
        roadmap_requests_collection.update_one(
            {'request_id': request_id},
            {
                '$set': {
                    'status': 'completed',
                    'completed_at': datetime.utcnow(),
                    'roadmap_id': roadmap_id
                }
            }
        )
        
        logger.info(f"Roadmap generated successfully: {roadmap_id} for user: {user_id}")
        
        return jsonify({
            'request_id': request_id,
            'roadmap_id': roadmap_id,
            'roadmap': roadmap_data,
            'saved': user_id is not None,
            'user_authenticated': current_user is not None
        })
        
    except Exception as e:
        logger.error(f"Roadmap generation error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Update request status to failed if we have a request_id
        if 'request_id' in locals():
            roadmap_requests_collection.update_one(
                {'request_id': request_id},
                {
                    '$set': {
                        'status': 'failed',
                        'error': str(e),
                        'failed_at': datetime.utcnow()
                    }
                }
            )
        
        return jsonify({'error': 'Failed to generate roadmap'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=port, debug=debug)