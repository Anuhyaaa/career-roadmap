"""
Authentication and User Management Routes
"""

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# MongoDB connection (will be initialized from main app)
db = None
users_collection = None

def init_auth_db(database):
    """Initialize database connection for auth module"""
    global db, users_collection
    db = database
    users_collection = db.users

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', data.get('full_name', '')).strip()
        
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
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Create new user
        user_doc = {
            'email': email,
            'name': name if name else email.split('@')[0],
            'password_hash': generate_password_hash(password),
            'created_at': datetime.utcnow(),
            'last_login': None,
            'is_active': True
        }
        
        result = users_collection.insert_one(user_doc)
        
        # Create session
        session['user_id'] = str(result.inserted_id)
        session['user_email'] = email
        
        # Return user data (excluding password)
        user_data = {
            'id': str(result.inserted_id),
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

@auth_bp.route('/login', methods=['POST'])
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
        user = users_collection.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        users_collection.update_one(
            {'_id': user['_id']},
            {'$set': {'last_login': datetime.utcnow()}}
        )
        
        # Create session
        session['user_id'] = str(user['_id'])
        session['user_email'] = email
        
        # Return user data
        user_data = {
            'id': str(user['_id']),
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

@auth_bp.route('/logout', methods=['POST'])
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

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user information"""
    try:
        logger.info(f"Auth check - Session data: {dict(session)}")
        
        if 'user_id' not in session:
            logger.info("No user_id in session")
            return jsonify({'error': 'Not authenticated'}), 401
        
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        
        if not user:
            logger.info(f"User not found for ID: {session['user_id']}")
            # Clear invalid session
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        # Return user data directly (not wrapped in 'user' object)
        user_data = {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at'].isoformat(),
            'last_login': user.get('last_login').isoformat() if user.get('last_login') else None
        }
        
        logger.info(f"Returning user data: {user_data}")
        return jsonify(user_data)
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({'error': 'Failed to get user information'}), 500

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if user has valid session"""
    try:
        if 'user_id' in session:
            user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
            if user and user.get('is_active', True):
                return jsonify({
                    'authenticated': True,
                    'user': {
                        'id': str(user['_id']),
                        'email': user['email'],
                        'name': user['name']
                    }
                })
        
        return jsonify({'authenticated': False})
        
    except Exception as e:
        logger.error(f"Check session error: {str(e)}")
        return jsonify({'authenticated': False})