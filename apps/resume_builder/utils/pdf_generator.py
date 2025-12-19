from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import io

class PDFGenerator:
    """
    Utility class to generate PDF resumes
    """
    
    @staticmethod
    def generate_resume_pdf(resume_data):
        """
        Generate a PDF resume from resume data
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = styles['Title']
        title = Paragraph(f"{resume_data['name']}", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Contact Info
        contact_style = styles['Normal']
        contact_info = f"Email: {resume_data['email']} | Phone: {resume_data['phone']}"
        contact = Paragraph(contact_info, contact_style)
        story.append(contact)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        heading_style = styles['Heading2']
        story.append(Paragraph("Professional Summary", heading_style))
        summary = Paragraph(resume_data['summary'], styles['Normal'])
        story.append(summary)
        story.append(Spacer(1, 0.2*inch))
        
        # Experience
        story.append(Paragraph("Work Experience", heading_style))
        for exp in resume_data['experience']:
            story.append(Paragraph(f"<b>{exp['title']}</b> - {exp['company']}", styles['Normal']))
            story.append(Paragraph(exp['duration'], styles['Normal']))
            story.append(Paragraph(exp['description'], styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Education
        story.append(Paragraph("Education", heading_style))
        for edu in resume_data['education']:
            story.append(Paragraph(f"<b>{edu['degree']}</b>", styles['Normal']))
            story.append(Paragraph(f"{edu['school']} - {edu['year']}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Skills
        story.append(Paragraph("Skills", heading_style))
        skills_text = ", ".join(resume_data['skills'])
        story.append(Paragraph(skills_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        pdf_value = buffer.getvalue()
        buffer.close()
        
        return pdf_value
    
    @staticmethod
    def generate_simple_pdf(content, filename):
        """
        Generate a simple PDF with basic content
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Split content into lines
        lines = content.split('\n')
        y_position = 750
        
        for line in lines:
            p.drawString(100, y_position, line)
            y_position -= 20
            
            # If we're near the bottom of the page, create a new page
            if y_position < 50:
                p.showPage()
                y_position = 750
        
        p.save()
        
        pdf_value = buffer.getvalue()
        buffer.close()
        
        return pdf_value