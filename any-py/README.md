# Career Roadmap Generator 🚀

**An AI-Powered Career Planning Platform for Students and Professionals**

A modern web application that generates personalized career learning roadmaps using artificial intelligence. Built with React frontend and designed for Flask backend integration.

## 📋 Project Overview

The Career Roadmap Generator helps users create structured, actionable career development plans by analyzing their interests, skills, and goals. The AI generates comprehensive roadmaps including skill progression paths, learning platforms, certifications, project ideas, and realistic timelines.

## 🏗️ Project Structure

```
career-roadmap-generator/
├── 📁 frontend/                 # React + Vite frontend application
│   ├── 📁 src/                 # Source code
│   │   ├── 📁 components/      # Reusable UI components
│   │   ├── 📁 pages/           # Main application pages
│   │   ├── 📁 contexts/        # React contexts (auth, etc.)
│   │   └── 📁 utils/           # Utility functions
│   ├── 📄 package.json         # Frontend dependencies
│   ├── 📄 tailwind.config.js   # Tailwind CSS configuration
│   ├── 📄 vite.config.js       # Vite build configuration
│   └── 📄 README-CA.md         # Comprehensive frontend guide
├── 📁 backend/                 # Flask backend (to be implemented)
│   ├── 📁 app/                 # Flask application
│   ├── 📁 models/              # Database models
│   ├── 📁 routes/              # API endpoints
│   └── 📄 requirements.txt     # Python dependencies
├── 📄 srs.txt                  # Software Requirements Specification
├── 📄 .gitignore               # Git ignore rules
└── 📄 README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend - future)
- **Git** for version control

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Open browser to http://localhost:5173
```

### Backend Setup (Coming Soon)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

## 🛠️ Technology Stack

### Frontend (✅ Completed)
- **React 19** - Modern UI library with hooks
- **Vite 7** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide Icons** - Beautiful icon library
- **Framer Motion** - Smooth animations

### Backend (🔄 In Progress)
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database (via Supabase)
- **OpenAI/Gemini API** - AI roadmap generation
- **JWT** - Authentication tokens
- **WeasyPrint** - PDF generation

## 📱 Features

### ✅ Implemented (Frontend)
- **Responsive Design** - Works on all devices
- **Interactive Forms** - Career assessment with validation
- **Results Display** - Tabbed roadmap presentation
- **Demo Authentication** - User login/signup flow
- **Smooth Animations** - Professional UI transitions
- **Error Handling** - Graceful error boundaries

### 🔄 In Development (Backend)
- **AI Integration** - Real roadmap generation
- **User Management** - Account creation and authentication
- **Data Persistence** - Save and retrieve roadmaps
- **PDF Export** - Download roadmaps as PDFs
- **Admin Dashboard** - Usage analytics and management

## 🎯 Current Status

**Phase 1: Frontend Development** ✅ **COMPLETE**
- All UI components implemented
- User flows and navigation working
- Responsive design across all devices
- Demo authentication system
- Ready for backend integration

**Phase 2: Backend Development** 🔄 **IN PROGRESS**
- API endpoint design
- Database schema implementation
- AI service integration
- Authentication system
- PDF generation service

## 📚 Documentation

- **[Frontend Guide](frontend/README-CA.md)** - Comprehensive guide for students and developers
- **[SRS Document](srs.txt)** - Complete software requirements specification
- **API Documentation** - Coming with backend implementation

## 🎓 Educational Value

This project demonstrates:
- **Modern Frontend Development** - React, Tailwind, responsive design
- **Full-Stack Architecture** - Frontend/backend separation
- **AI Integration** - Working with language models
- **Database Design** - User management and data persistence
- **Professional Practices** - Git workflow, documentation, testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Anuhya** - Frontend Developer & UI/UX Designer
- **Project Mentor** - Technical guidance and code review

## 🔗 Links

- **Live Demo** - Coming soon
- **API Documentation** - Coming with backend
- **Design System** - Documented in frontend README

## 📞 Support

For questions or support:
- Create an issue in this repository
- Check the comprehensive [Frontend Guide](frontend/README-CA.md)
- Review the [SRS Document](srs.txt) for detailed requirements

---

**Built with ❤️ for career development and learning**