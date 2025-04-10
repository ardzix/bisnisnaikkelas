from django_q.tasks import async_task
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
import os
from decimal import Decimal
from .models import BusinessAssessment, ReadinessAssessment, ReadinessAnswer
from .scoring import calculate_assessment

def calculate_readiness_score(assessment_id: int):
    """
    Calculate the readiness score for an assessment.
    The score is calculated based on the weighted average of answers.
    """
    try:
        assessment = ReadinessAssessment.objects.get(id=assessment_id)
        answers = ReadinessAnswer.objects.filter(assessment=assessment).select_related('question')
        
        if not answers.exists():
            return
        
        total_weight = Decimal('0')
        weighted_score = Decimal('0')
        
        for answer in answers:
            weight = answer.question.weight
            total_weight += weight
            
            # Calculate score based on answer
            if answer.answer == 'yes':
                score = Decimal('1.0')
            elif answer.answer == 'partial':
                score = Decimal('0.5')
            else:  # no
                score = Decimal('0')
            
            weighted_score += weight * score
        
        # Calculate final score (0-100)
        if total_weight > 0:
            final_score = (weighted_score / total_weight) * 100
            assessment.score = final_score
            assessment.save()
    
    except ReadinessAssessment.DoesNotExist:
        pass

def generate_pdf_report(assessment_id: str):
    """Generate PDF report for business assessment"""
    try:
        assessment = BusinessAssessment.objects.get(id=assessment_id)
        
        # Calculate scores and business level using the new scoring system
        scores, level, recommendations = calculate_assessment(assessment)
        
        # Prepare context for template
        context = {
            'assessment': assessment,
            'scores': scores,
            'level': level,
            'recommendations': recommendations
        }
        
        # Render HTML template
        html_string = render_to_string('readiness/report_template.html', context)
        
        # Generate PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        
        # Save PDF file
        filename = f'report_{assessment_id}.pdf'
        filepath = os.path.join(settings.MEDIA_ROOT, 'reports', filename)
        
        with open(filepath, 'wb') as f:
            f.write(pdf)
        
        # Update assessment
        assessment.report_pdf = f'reports/{filename}'
        assessment.report_ready = True
        assessment.save()
        
    except Exception as e:
        # Log error and update assessment
        assessment = BusinessAssessment.objects.get(id=assessment_id)
        assessment.report_ready = True  # Mark as ready to prevent infinite polling
        assessment.save()
        raise e

def schedule_pdf_generation(assessment_id: str):
    """Schedule PDF generation task"""
    async_task(generate_pdf_report, assessment_id) 