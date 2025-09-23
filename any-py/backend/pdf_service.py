"""
PDF Export Service
"""

from flask import Blueprint, request, jsonify, session, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import logging
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import io

logger = logging.getLogger(__name__)

# Create blueprint for PDF routes
pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

# MongoDB connection (will be initialized from main app)
db = None
roadmaps_collection = None
roadmap_requests_collection = None

def init_pdf_db(database):
    """Initialize database connection for PDF module"""
    global db, roadmaps_collection, roadmap_requests_collection
    db = database
    roadmaps_collection = db.roadmaps
    roadmap_requests_collection = db.roadmap_requests

def get_current_user_id():
    """Get current user ID from session"""
    return session.get('user_id')

class PDFGenerator:
    """PDF generation utility class"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f2937')
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#374151')
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#4b5563')
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
        
        # List item style
        self.list_style = ParagraphStyle(
            'ListItem',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=4
        )
    
    def generate_roadmap_pdf(self, roadmap_data, form_data):
        """Generate PDF from roadmap data"""
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Title
        story.append(Paragraph("Career Roadmap", self.title_style))
        story.append(Spacer(1, 12))
        
        # User Information Section
        story.append(Paragraph("Personal Information", self.subtitle_style))
        
        user_info_data = [
            ['Interests:', form_data.get('interests', 'Not specified')],
            ['Education Level:', self._format_education_level(form_data.get('education', 'Not specified'))],
            ['Current Skills:', form_data.get('currentSkills', 'Not specified')],
            ['Career Goal:', form_data.get('careerGoal', 'Not specified')],
            ['Generated On:', datetime.utcnow().strftime('%B %d, %Y')]
        ]
        
        user_info_table = Table(user_info_data, colWidths=[1.5*inch, 4*inch])
        user_info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(user_info_table)
        story.append(Spacer(1, 20))
        
        # Skill Path Section
        if roadmap_data.get('skill_path'):
            story.append(Paragraph("Learning Path", self.subtitle_style))
            
            for i, skill in enumerate(roadmap_data['skill_path'], 1):
                story.append(Paragraph(f"{i}. {skill.get('name', 'Unknown Skill')}", self.section_style))
                story.append(Paragraph(skill.get('description', 'No description available'), self.body_style))
                
                if skill.get('prerequisites'):
                    prereq_text = "Prerequisites: " + ", ".join(skill['prerequisites'])
                    story.append(Paragraph(prereq_text, self.list_style))
                
                duration = skill.get('estimated_duration_weeks', 0)
                if duration:
                    story.append(Paragraph(f"Estimated Duration: {duration} weeks", self.list_style))
                
                story.append(Spacer(1, 8))
        
        # Learning Platforms Section
        if roadmap_data.get('platforms'):
            story.append(Paragraph("Recommended Learning Platforms", self.subtitle_style))
            
            platform_data = [['Platform', 'Type', 'Rationale']]
            for platform in roadmap_data['platforms']:
                platform_data.append([
                    platform.get('name', 'Unknown'),
                    platform.get('type', 'Unknown'),
                    platform.get('rationale', 'No rationale provided')
                ])
            
            platform_table = Table(platform_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
            platform_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
            ]))
            
            story.append(platform_table)
            story.append(Spacer(1, 20))
        
        # Certifications Section
        if roadmap_data.get('certifications'):
            story.append(Paragraph("Recommended Certifications", self.subtitle_style))
            
            for cert in roadmap_data['certifications']:
                story.append(Paragraph(f"• {cert.get('name', 'Unknown Certification')}", self.section_style))
                story.append(Paragraph(f"Provider: {cert.get('provider', 'Unknown')}", self.list_style))
                story.append(Paragraph(f"Level: {cert.get('level', 'Unknown')}", self.list_style))
                story.append(Paragraph(f"Rationale: {cert.get('rationale', 'No rationale provided')}", self.body_style))
                story.append(Spacer(1, 8))
        
        # Project Ideas Section
        if roadmap_data.get('project_ideas'):
            story.append(PageBreak())
            story.append(Paragraph("Project Ideas", self.subtitle_style))
            
            for level, projects in roadmap_data['project_ideas'].items():
                if projects:
                    story.append(Paragraph(f"{level.capitalize()} Projects", self.section_style))
                    
                    for project in projects:
                        story.append(Paragraph(f"• {project.get('title', 'Untitled Project')}", self.list_style))
                        story.append(Paragraph(project.get('description', 'No description available'), self.body_style))
                        
                        if project.get('learning_objectives'):
                            objectives = ", ".join(project['learning_objectives'])
                            story.append(Paragraph(f"Learning Objectives: {objectives}", self.list_style))
                        
                        story.append(Spacer(1, 6))
                    
                    story.append(Spacer(1, 12))
        
        # Timeline Section
        if roadmap_data.get('timeline'):
            story.append(Paragraph("Timeline", self.subtitle_style))
            
            timeline_data = [['Phase', 'Duration', 'Focus Skills', 'Key Milestones']]
            for phase in roadmap_data['timeline']:
                phase_title = f"Phase {phase.get('phase_number', 'N/A')}: {phase.get('title', 'Untitled')}"
                duration = f"{phase.get('duration_weeks', 0)} weeks"
                focus_skills = ", ".join(phase.get('focus_skills', []))
                milestones = ", ".join(phase.get('milestones', []))
                
                timeline_data.append([phase_title, duration, focus_skills, milestones])
            
            timeline_table = Table(timeline_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 2*inch])
            timeline_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            story.append(timeline_table)
            story.append(Spacer(1, 20))
        
        # Notes Section
        if roadmap_data.get('notes'):
            story.append(Paragraph("Additional Notes", self.subtitle_style))
            for note in roadmap_data['notes']:
                story.append(Paragraph(f"• {note}", self.list_style))
            story.append(Spacer(1, 20))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = "This roadmap was generated by Career Roadmap Generator. Please verify all recommendations and adapt them to your specific needs and circumstances."
        story.append(Paragraph(footer_text, self.body_style))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer
    
    def _format_education_level(self, education):
        """Format education level for display"""
        education_map = {
            'high-school': 'High School / Secondary',
            'associate': 'Associate Degree',
            'bachelors': 'Bachelor\'s Degree',
            'masters': 'Master\'s Degree',
            'phd': 'PhD / Doctorate',
            'bootcamp': 'Bootcamp / Certification',
            'self-taught': 'Self-Taught',
            'other': 'Other'
        }
        return education_map.get(education, education)

@pdf_bp.route('/export/<roadmap_id>', methods=['GET'])
def export_roadmap_pdf(roadmap_id):
    """Export roadmap as PDF"""
    try:
        user_id = get_current_user_id()
        
        # Build query to find roadmap
        query = {'_id': ObjectId(roadmap_id)}
        
        # If user is authenticated, allow access to their roadmaps and guest roadmaps
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
        
        if not request_data:
            return jsonify({'error': 'Original request data not found'}), 404
        
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_buffer = pdf_generator.generate_roadmap_pdf(
            roadmap['roadmap_data'],
            request_data['form_data']
        )
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=career_roadmap_{roadmap_id}.pdf'
        
        logger.info(f"PDF exported for roadmap: {roadmap_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error exporting PDF: {str(e)}")
        return jsonify({'error': 'Failed to export PDF'}), 500