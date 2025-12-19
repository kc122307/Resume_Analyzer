import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import io
import os
from apps.users.models import Profile
from ai_resume_platform.utils.ai_service import AIService
from .utils.pdf_generator import PDFGenerator
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

@login_required
def builder(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.resume_url:
        messages.error(request, 'Please upload a resume first.')
        return redirect('resume_upload')
    
    # Increment resumes built counter
    if 'resumes_built' in request.session:
        request.session['resumes_built'] += 1
    else:
        request.session['resumes_built'] = 1
    
    return render(request, 'resume_builder/builder.html', {'profile': profile})

@login_required
def generate_resume(request):
    if request.method == 'POST':
        try:
            # Get form data
            template_type = request.POST.get('template_type', '')
            target_company = request.POST.get('target_company', '')
            target_job_role = request.POST.get('target_job_role', '')
            job_description = request.POST.get('job_description', '')
            skills_to_highlight = request.POST.get('skills_to_highlight', '')
            projects = request.POST.get('projects', '')
            achievements = request.POST.get('achievements', '')
            experience_level = request.POST.get('experience_level', '')
            additional_notes = request.POST.get('additional_notes', '')
            
            profile = Profile.objects.get(user=request.user)
            
            if not profile.resume_url:
                return JsonResponse({'error': 'No resume uploaded'}, status=400)
            
            # Initialize AI service
            ai_service = AIService()
            
            # Prepare user inputs for AI service
            user_inputs = {
                'template_type': template_type,
                'target_company': target_company,
                'target_job_role': target_job_role,
                'job_description': job_description,
                'skills_to_highlight': skills_to_highlight,
                'projects': projects,
                'achievements': achievements,
                'experience_level': experience_level,
                'additional_notes': additional_notes
            }
            
            # Call AI service to generate resume
            resume_data = ai_service.generate_optimized_resume(profile.resume_url, user_inputs)
            
            # Check if there was an error
            if 'error' in resume_data:
                return JsonResponse({'error': resume_data['error']}, status=500)
            
            # Store resume data in session for PDF generation
            request.session['generated_resume'] = resume_data
            
            # Return PDF filename for download and preview data
            filename = f"{request.user.username}_resume.pdf"
            return JsonResponse({'filename': filename, 'preview_data': resume_data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def download_resume(request, filename):
    try:
        # Get the generated resume data from session
        resume_data = request.session.get('generated_resume', None)
        
        if not resume_data or 'pdf_resume' not in resume_data:
            messages.error(request, 'No resume data found. Please generate a resume first.')
            return redirect('builder')
        
        pdf_resume = resume_data['pdf_resume']
        
        # Generate PDF using the PDFGenerator utility
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Header section
        header = pdf_resume.get('header', {})
        name = header.get('name', 'Name')
        title = header.get('title', 'Professional Title')
        summary = header.get('summary', '')
        
        # Name
        title_style = styles['Title']
        story.append(Paragraph(name, title_style))
        
        # Title
        subtitle_style = styles['Heading2']
        story.append(Paragraph(title, subtitle_style))
        
        # Summary
        if summary:
            story.append(Paragraph(summary, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Skills
        skills = pdf_resume.get('skills', [])
        if skills:
            story.append(Paragraph("Skills", styles['Heading2']))
            skills_text = ", ".join(skills)
            story.append(Paragraph(skills_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Experience
        experiences = pdf_resume.get('experience', [])
        if experiences:
            story.append(Paragraph("Experience", styles['Heading2']))
            for exp in experiences:
                company = exp.get('company', '')
                role = exp.get('role', '')
                duration = exp.get('duration', '')
                bullets = exp.get('bullets', [])
                
                # Role and company
                if role and company:
                    story.append(Paragraph(f"<b>{role}</b> - {company}", styles['Normal']))
                elif role:
                    story.append(Paragraph(f"<b>{role}</b>", styles['Normal']))
                elif company:
                    story.append(Paragraph(f"{company}", styles['Normal']))
                
                # Duration
                if duration:
                    story.append(Paragraph(duration, styles['Normal']))
                
                # Bullets
                for bullet in bullets:
                    story.append(Paragraph(f"• {bullet}", styles['Normal']))
                
                story.append(Spacer(1, 0.1*inch))
        
        # Projects
        projects = pdf_resume.get('projects', [])
        if projects:
            story.append(Paragraph("Projects", styles['Heading2']))
            for proj in projects:
                name = proj.get('name', '')
                description = proj.get('description', '')
                
                if name:
                    story.append(Paragraph(f"<b>{name}</b>", styles['Normal']))
                if description:
                    story.append(Paragraph(description, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Education
        educations = pdf_resume.get('education', [])
        if educations:
            story.append(Paragraph("Education", styles['Heading2']))
            for edu in educations:
                degree = edu.get('degree', '')
                institution = edu.get('institution', '')
                year = edu.get('year', '')
                
                if degree:
                    story.append(Paragraph(f"<b>{degree}</b>", styles['Normal']))
                if institution and year:
                    story.append(Paragraph(f"{institution}, {year}", styles['Normal']))
                elif institution:
                    story.append(Paragraph(institution, styles['Normal']))
                elif year:
                    story.append(Paragraph(year, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Certifications
        certifications = pdf_resume.get('certifications', [])
        if certifications:
            story.append(Paragraph("Certifications", styles['Heading2']))
            cert_text = ", ".join(certifications)
            story.append(Paragraph(cert_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        pdf_value = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf_value, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        messages.error(request, f'Error generating resume: {str(e)}')
        return redirect('builder')