# Career Roadmap Generator

A full-stack application that generates personalized career roadmaps using AI.

## Features

- 🤖 AI-powered career roadmap generation using Google Gemini
- 👤 User authentication and profile management
- 📈 Personalized skill paths and timelines
- 📱 Responsive React frontend with Tailwind CSS
- 🔐 Secure session-based authentication
- 📄 PDF export functionality
- 🗃️ MongoDB data persistence

## Tech Stack

### Frontend
- React 19+ with Vite
- Tailwind CSS for styling
- React Router for navigation
- Lucide React for icons
- Framer Motion for animations

### Backend
- Python Flask API
- MongoDB for data storage
- Google Gemini AI for roadmap generation
- Flask-CORS for cross-origin requests
- Session-based authentication

## Deployment

### Frontend (Vercel)
The frontend is deployed on Vercel with automatic builds from the main branch.

### Backend (Vercel)
The backend is deployed on Vercel as a Python serverless function.

## Environment Variables

### Frontend (.env.production)
```
VITE_API_BASE_URL=https://your-backend-url.vercel.app/api
```

### Backend (Vercel Environment Variables)
```
SECRET_KEY=your-secret-key
MONGO_URI=your-mongodb-connection-string
GEMINI_API_KEY=your-google-gemini-api-key
FRONTEND_URL=https://your-frontend-url.vercel.app
```

## Local Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout
- `POST /api/generate-roadmap` - Generate career roadmap
- `GET /api/roadmaps/history` - Get user's roadmap history
- `GET /api/roadmaps/{id}` - Get specific roadmap
- `DELETE /api/roadmaps/{id}` - Delete roadmap

## License

MIT License
