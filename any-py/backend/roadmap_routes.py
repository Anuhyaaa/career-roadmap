"""
Roadmap Management Routes
"""

from flask import Blueprint, request, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Create blueprint for roadmap routes
roadmap_bp = Blueprint('roadmap', __name__, url_prefix='/api/roadmaps')

# MongoDB connection (will be initialized from main app)
db = None
roadmaps_collection = None
roadmap_requests_collection = None

def init_roadmap_db(database):
    """Initialize database connection for roadmap module"""
    global db, roadmaps_collection, roadmap_requests_collection
    db = database
    roadmaps_collection = db.roadmaps
    roadmap_requests_collection = db.roadmap_requests

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

def get_current_user_id():
    """Get current user ID from session"""
    return session.get('user_id')

@roadmap_bp.route('/history', methods=['GET'])
def get_user_roadmap_history():
    """Get all roadmaps for the current user"""
    try:
        user_id = get_current_user_id()
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        skip = (page - 1) * limit
        
        # Query user's roadmaps
        query = {'user_id': ObjectId(user_id)}
        
        # Get total count
        total_count = roadmaps_collection.count_documents(query)
        
        # Get roadmaps with pagination
        roadmaps_cursor = roadmaps_collection.find(query).sort('created_at', -1).skip(skip).limit(limit)
        roadmaps = list(roadmaps_cursor)
        
        # Serialize and format roadmaps
        formatted_roadmaps = []
        for roadmap in roadmaps:
            # Get the original request data for context
            request_data = roadmap_requests_collection.find_one({'request_id': roadmap['request_id']})
            
            formatted_roadmap = {
                'id': str(roadmap['_id']),
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
            formatted_roadmaps.append(formatted_roadmap)
        
        return jsonify({
            'roadmaps': formatted_roadmaps,
            'pagination': {
                'page': page,
                'limit': limit,
                'total_count': total_count,
                'total_pages': (total_count + limit - 1) // limit,
                'has_next': page * limit < total_count,
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching roadmap history: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap history'}), 500

@roadmap_bp.route('/<roadmap_id>', methods=['GET'])
def get_roadmap_details(roadmap_id):
    """Get detailed roadmap by ID"""
    try:
        user_id = get_current_user_id()
        
        # Build query
        query = {'_id': ObjectId(roadmap_id)}
        
        # If user is authenticated, allow access to their roadmaps
        # If not authenticated, only allow access to guest roadmaps
        if user_id:
            query['$or'] = [
                {'user_id': ObjectId(user_id)},
                {'user_id': None}  # Guest roadmaps
            ]
        else:
            query['user_id'] = None  # Only guest roadmaps
        
        roadmap = roadmaps_collection.find_one(query)
        
        if not roadmap:
            return jsonify({'error': 'Roadmap not found or access denied'}), 404
        
        # Get the original request data
        request_data = roadmap_requests_collection.find_one({'request_id': roadmap['request_id']})
        
        response_data = {
            'id': str(roadmap['_id']),
            'request_id': roadmap['request_id'],
            'created_at': roadmap['created_at'].isoformat(),
            'form_data': request_data['form_data'] if request_data else {},
            'roadmap': roadmap['roadmap_data'],
            'is_owner': str(roadmap.get('user_id')) == user_id if roadmap.get('user_id') else False
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error fetching roadmap details: {str(e)}")
        return jsonify({'error': 'Failed to fetch roadmap details'}), 500

@roadmap_bp.route('/<roadmap_id>', methods=['DELETE'])
def delete_roadmap(roadmap_id):
    """Delete a roadmap (only by owner)"""
    try:
        user_id = get_current_user_id()
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check if roadmap exists and belongs to user
        roadmap = roadmaps_collection.find_one({
            '_id': ObjectId(roadmap_id),
            'user_id': ObjectId(user_id)
        })
        
        if not roadmap:
            return jsonify({'error': 'Roadmap not found or access denied'}), 404
        
        # Delete the roadmap
        roadmaps_collection.delete_one({'_id': ObjectId(roadmap_id)})
        
        # Also delete the associated request
        roadmap_requests_collection.delete_one({'request_id': roadmap['request_id']})
        
        logger.info(f"Roadmap deleted: {roadmap_id} by user: {user_id}")
        
        return jsonify({'message': 'Roadmap deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting roadmap: {str(e)}")
        return jsonify({'error': 'Failed to delete roadmap'}), 500

@roadmap_bp.route('/stats', methods=['GET'])
def get_user_stats():
    """Get user's roadmap statistics"""
    try:
        user_id = get_current_user_id()
        
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Get user's roadmap count
        total_roadmaps = roadmaps_collection.count_documents({'user_id': ObjectId(user_id)})
        
        # Get roadmaps created in the last 30 days
        thirty_days_ago = datetime.utcnow() - datetime.timedelta(days=30)
        recent_roadmaps = roadmaps_collection.count_documents({
            'user_id': ObjectId(user_id),
            'created_at': {'$gte': thirty_days_ago}
        })
        
        # Get most recent roadmap
        latest_roadmap = roadmaps_collection.find_one(
            {'user_id': ObjectId(user_id)},
            sort=[('created_at', -1)]
        )
        
        # Calculate total estimated learning time
        user_roadmaps = roadmaps_collection.find({'user_id': ObjectId(user_id)})
        total_learning_weeks = 0
        
        for roadmap in user_roadmaps:
            timeline = roadmap['roadmap_data'].get('timeline', [])
            for phase in timeline:
                total_learning_weeks += phase.get('duration_weeks', 0)
        
        stats = {
            'total_roadmaps': total_roadmaps,
            'recent_roadmaps': recent_roadmaps,
            'total_estimated_learning_weeks': total_learning_weeks,
            'latest_roadmap_date': latest_roadmap['created_at'].isoformat() if latest_roadmap else None
        }
        
        return jsonify({'stats': stats})
        
    except Exception as e:
        logger.error(f"Error fetching user stats: {str(e)}")
        return jsonify({'error': 'Failed to fetch user statistics'}), 500