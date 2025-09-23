"""
Career Roadmap Generator Backend
Flask application with MongoDB integration
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
import google.generativeai as genai
from typing import Dict, Any, Optional
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Enable CORS for frontend
CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

# MongoDB connection
MONGO_URI = "mongodb+srv://anuhya:anuhya123@cluster0.1yxhld9.mongodb.net/career?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.career

# Collections
users_collection = db.users
roadmap_requests_collection = db.roadmap_requests
roadmaps_collection = db.roadmaps

# Google Gemini API configuration
GEMINI_API_KEY = "AIzaSyAFcFv5efZN6lhp-dFM3dzCEJZexjQb-Rk"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

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
    if 'user_id' in session:
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        return serialize_mongo_doc(user)
    return None

# AI Service Functions
def construct_ai_prompt(form_data: Dict[str, Any]) -> str:
    """Construct the prompt for AI model"""
    
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

    return f"{system_instruction}\n\n{user_data}"

def generate_roadmap_with_ai(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate career roadmap using Google Gemini AI"""
    try:
        prompt = construct_ai_prompt(form_data)
        
        # Generate content using Gemini
        response = model.generate_content(prompt)
        
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

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected' if client.admin.command('ping') else 'disconnected'
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
                'user_authenticated': current_user is not None
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

@app.route('/api/roadmap/<roadmap_id>', methods=['GET'])
def get_roadmap(roadmap_id):
    """Get a specific roadmap by ID"""
    try:
        current_user = get_current_user()
        
        # Find roadmap
        query = {'_id': ObjectId(roadmap_id)}
        
        # If user is authenticated, only show their roadmaps or public ones
        if current_user:
            query['$or'] = [
                {'user_id': ObjectId(current_user['id'])},
                {'user_id': None}  # Guest roadmaps
            ]
        else:
            query['user_id'] = None  # Only guest roadmaps for non-authenticated users
        
        roadmap = roadmaps_collection.find_one(query)
        
        if not roadmap:
            return jsonify({'error': 'Roadmap not found'}), 404
        
        return jsonify({
            'roadmap': serialize_mongo_doc(roadmap)
        })
        
    except Exception as e:
        logger.error(f"Error fetching roadmap: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)