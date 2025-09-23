# Career Roadmap Generator - Backend API

A Flask-based REST API that generates personalized career roadmaps using Google Gemini AI and stores data in MongoDB.

## Features

- **AI-Powered Roadmap Generation**: Uses Google Gemini AI to create personalized career roadmaps
- **User Authentication**: Register, login, and session management
- **Roadmap Management**: Save, retrieve, and manage career roadmaps
- **PDF Export**: Export roadmaps as professionally formatted PDF documents
- **MongoDB Integration**: Secure data storage with MongoDB Atlas

## API Endpoints

### Health Check
- `GET /api/health` - Check API health and database connectivity

### AI & Roadmap Generation
- `POST /api/generate-roadmap` - Generate a new career roadmap using AI
- `GET /api/roadmap/<roadmap_id>` - Get a specific roadmap by ID

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user information
- `GET /api/auth/check-session` - Check authentication status

### Roadmap Management
- `GET /api/roadmaps/history` - Get user's roadmap history (paginated)
- `GET /api/roadmaps/<roadmap_id>` - Get detailed roadmap information
- `DELETE /api/roadmaps/<roadmap_id>` - Delete a roadmap (owner only)
- `GET /api/roadmaps/stats` - Get user's roadmap statistics

### PDF Export
- `GET /api/pdf/export/<roadmap_id>` - Export roadmap as PDF

## Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the configuration values:
     ```env
     MONGO_URI=your_mongodb_connection_string
     GEMINI_API_KEY=your_google_gemini_api_key
     SECRET_KEY=your_secret_key_for_sessions
     ```

6. **Run the application**
   ```bash
   python main.py
   ```
   
   Or use the batch file on Windows:
   ```bash
   run.bat
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB connection string | Required |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `SECRET_KEY` | Flask session secret key | Required |
| `FRONTEND_URL` | Frontend URL for CORS | `http://localhost:5173` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `FLASK_DEBUG` | Debug mode | `True` |

### Database Schema

The application uses three main MongoDB collections:

1. **users** - User authentication data
2. **roadmap_requests** - Request logs and form data
3. **roadmaps** - Generated roadmap data

## API Usage Examples

### Generate Roadmap
```javascript
POST /api/generate-roadmap
Content-Type: application/json

{
  "interests": "web development, javascript",
  "education": "bachelors",
  "currentSkills": "HTML, CSS, basic JavaScript",
  "careerGoal": "Full-stack developer"
}
```

### User Registration
```javascript
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

### Get Roadmap History
```javascript
GET /api/roadmaps/history?page=1&limit=10
```

## Error Handling

The API returns consistent error responses:

```javascript
{
  "error": "Error message",
  "details": "Additional error details (in development)"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CORS protection
- Input validation and sanitization
- Environment-based configuration

## Development

### Project Structure
```
backend/
├── main.py              # Main application file
├── auth.py              # Authentication routes
├── roadmap_routes.py    # Roadmap management routes
├── pdf_service.py       # PDF export functionality
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration
├── run.bat             # Windows startup script
└── README.md           # This file
```

### Adding New Features

1. Create new route modules following the blueprint pattern
2. Initialize database connections using the init functions
3. Register blueprints in `main.py`
4. Update this README with new endpoints

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check your MongoDB URI in `.env`
   - Ensure your IP is whitelisted in MongoDB Atlas
   - Verify network connectivity

2. **Gemini API Errors**
   - Verify your API key is correct
   - Check API quota and billing
   - Ensure proper API permissions

3. **CORS Issues**
   - Update `FRONTEND_URL` in `.env`
   - Check browser console for specific CORS errors

### Logs

The application logs important events and errors. Check the console output for debugging information.

## License

This project is part of the Career Roadmap Generator application.