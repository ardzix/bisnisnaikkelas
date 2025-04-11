from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import BusinessAssessment, UserProfile
from .scoring import calculate_assessment
from .tasks import schedule_pdf_generation
import json
import requests
from google.cloud import recaptchaenterprise_v1
import logging
import os
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
User = get_user_model()

def home(request):
    """Render the home page"""
    return render(request, 'home.html')

def sitemap(request):
    """Render the sitemap page"""
    return render(request, 'sitemap.html')

def assessment_form(request):
    """Render the assessment form"""
    return render(request, 'readiness/form.html', {
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
    })

def verify_recaptcha_token(token, action):
    """Verify reCAPTCHA token with Google's Enterprise API"""
    try:
        # Log environment variables and settings
        logger.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
        logger.info(f"GOOGLE_CLOUD_PROJECT: {settings.GOOGLE_CLOUD_PROJECT}")
        logger.info(f"RECAPTCHA_SITE_KEY: {settings.RECAPTCHA_SITE_KEY}")
        
        client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()
        project_name = f"projects/{settings.GOOGLE_CLOUD_PROJECT}"
        
        # Create assessment
        assessment = recaptchaenterprise_v1.Assessment()
        assessment.event = recaptchaenterprise_v1.Event()
        assessment.event.site_key = settings.RECAPTCHA_SITE_KEY
        assessment.event.token = token
        assessment.event.expected_action = action
        
        request = recaptchaenterprise_v1.CreateAssessmentRequest()
        request.parent = project_name
        request.assessment = assessment
        
        logger.info("Sending assessment request to Google reCAPTCHA Enterprise API")
        response = client.create_assessment(request)
        logger.info(f"Received response from Google reCAPTCHA Enterprise API: {response}")
        
        # Check if the token is valid
        if not response.token_properties.valid:
            logger.error("Invalid reCAPTCHA token")
            return False, "Invalid reCAPTCHA token"
        
        # Check if the action matches
        if response.token_properties.action != action:
            logger.error(f"Action mismatch. Expected: {action}, Got: {response.token_properties.action}")
            return False, "Action name doesn't match"
        
        # Check the score
        score = response.risk_analysis.score
        logger.info(f"reCAPTCHA score: {score}")
        if score < 0.5:  # You can adjust this threshold
            logger.warning(f"Score too low: {score}")
            return False, "Score too low"
        
        return True, None
        
    except Exception as e:
        logger.exception("Error verifying reCAPTCHA token")
        return False, str(e)

@require_http_methods(["POST"])
def submit_assessment(request):
    """Handle form submission and create assessment"""
    # Verify reCAPTCHA Express token
    token = request.POST.get('recaptcha-token')
    if not token:
        return JsonResponse({'error': 'reCAPTCHA token is required'}, status=400)
    
    success, error = verify_recaptcha_token(token, 'submit')
    if not success:
        return JsonResponse({'error': f'reCAPTCHA verification failed: {error}'}, status=400)
    
    try:
        # Create assessment from form data
        assessment = BusinessAssessment.objects.create(
            business_name=request.POST['business_name'],
            business_type=request.POST['business_type'],
            year_started=int(request.POST['year_started']),
            employee_count=int(request.POST['employee_count']),
            annual_revenue=float(request.POST['annual_revenue']),
            
            # Financial Information
            has_financial_records=request.POST.get('has_financial_records') == 'on',
            has_invoice_system=request.POST.get('has_invoice_system') == 'on',
            uses_financial_software=request.POST.get('uses_financial_software') == 'on',
            has_cashflow_forecast=request.POST.get('has_cashflow_forecast') == 'on',
            has_tax_calculation_practice=request.POST.get('has_tax_calculation_practice') == 'on',
            
            # Digital Presence
            has_website=request.POST.get('has_website') == 'on',
            has_online_store=request.POST.get('has_online_store') == 'on',
            has_social_media=request.POST.get('has_social_media') == 'on',
            is_social_media_active=request.POST.get('is_social_media_active') == 'on',
            uses_digital_ads=request.POST.get('uses_digital_ads') == 'on',
            uses_crm_or_marketing_tools=request.POST.get('uses_crm_or_marketing_tools') == 'on',
            
            # Legal Documentation
            has_npwp=request.POST.get('has_npwp') == 'on',
            has_business_license=request.POST.get('has_business_license') == 'on',
            has_profit_loss_statement=request.POST.get('has_profit_loss_statement') == 'on',
            has_balance_sheet=request.POST.get('has_balance_sheet') == 'on',
            has_contract_templates=request.POST.get('has_contract_templates') == 'on',
            registered_with_government_platforms=request.POST.get('registered_with_government_platforms') == 'on',
            
            # Operational
            has_sop_documentation=request.POST.get('has_sop_documentation') == 'on',
            has_team_structure=request.POST.get('has_team_structure') == 'on',
            
            # Strategy
            has_vision_and_mission=request.POST.get('has_vision_and_mission') == 'on',
            has_business_plan=request.POST.get('has_business_plan') == 'on',
            has_defined_target_market=request.POST.get('has_defined_target_market') == 'on',
            has_unique_value_proposition=request.POST.get('has_unique_value_proposition') == 'on',
            
            # Risk & Compliance
            has_data_backup=request.POST.get('has_data_backup') == 'on',
            has_been_audited=request.POST.get('has_been_audited') == 'on',
            has_third_party_contracts=request.POST.get('has_third_party_contracts') == 'on',
            has_tax_risk_management=request.POST.get('has_tax_risk_management') == 'on',
            has_internal_controls=request.POST.get('has_internal_controls') == 'on',
            
            # Technology
            uses_inventory_software=request.POST.get('uses_inventory_software') == 'on',
            can_operate_remotely=request.POST.get('can_operate_remotely') == 'on',
            uses_automation_or_integration=request.POST.get('uses_automation_or_integration') == 'on',
            has_internal_dashboard_or_kpi_system=request.POST.get('has_internal_dashboard_or_kpi_system') == 'on',
            
            # Market Access
            sells_nationally_or_internationally=request.POST.get('sells_nationally_or_internationally') == 'on',
            attends_trade_expos=request.POST.get('attends_trade_expos') == 'on',
            has_reseller_or_distributor=request.POST.get('has_reseller_or_distributor') == 'on',
            has_partnership_program=request.POST.get('has_partnership_program') == 'on',
            
            # Process Maturity
            has_payroll_system=request.POST.get('has_payroll_system') == 'on',
            has_quality_control_process=request.POST.get('has_quality_control_process') == 'on',
            has_employee_handbook_or_sop=request.POST.get('has_employee_handbook_or_sop') == 'on',
            has_formal_onboarding=request.POST.get('has_formal_onboarding') == 'on',
            
            # Business Goals
            business_goals=request.POST['business_goals'],
            interested_in_mentoring=request.POST.get('interested_in_mentoring') == 'on'
        )
        
        # Calculate scores and business level using the new scoring system
        scores, business_level, recommendations = calculate_assessment(assessment)
        
        # Update assessment with results
        assessment.business_level = business_level
        assessment.recommendations = recommendations
        
        # Store individual scores for backward compatibility
        for category, score in scores.items():
            if category != 'total':
                setattr(assessment, f"{category}_score", score)
        
        assessment.total_score = scores['total']
        assessment.save()
        
        # If user is authenticated and has a profile, associate assessment
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                profile.assessments.add(assessment)
            except UserProfile.DoesNotExist:
                # Create profile if it doesn't exist
                profile = UserProfile.objects.create(
                    user=request.user,
                    full_name=request.user.email.split('@')[0],  # Default name from email
                    phone_number=''
                )
                profile.assessments.add(assessment)  # Add assessment after creation
        
        # Schedule PDF generation
        schedule_pdf_generation(str(assessment.id))
        
        # Return JSON response with processing URL
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('readiness:processing', args=[str(assessment.id)])
        })
        
    except Exception as e:
        logger.exception("Assessment submission error")
        return JsonResponse({'error': str(e)}, status=400)

def processing(request, assessment_id):
    """Show processing page while PDF is being generated"""
    assessment = get_object_or_404(BusinessAssessment, id=assessment_id)
    # Store assessment ID in session for later association
    request.session['pending_assessment_id'] = str(assessment_id)
    return render(request, 'readiness/processing.html', {'assessment': assessment})

@require_http_methods(["GET"])
def check_status(request, assessment_id):
    """Check if PDF is ready"""
    assessment = get_object_or_404(BusinessAssessment, id=assessment_id)
    return JsonResponse({
        'ready': assessment.report_ready,
        'download_url': assessment.report_pdf.url if assessment.report_ready else None
    })

def download_report(request, assessment_id):
    """Serve the generated PDF report"""
    assessment = get_object_or_404(BusinessAssessment, id=assessment_id)
    if not assessment.report_ready or not assessment.report_pdf:
        return JsonResponse({'error': 'Report not ready'}, status=404)
    
    try:
        file = default_storage.open(assessment.report_pdf.name)
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="assessment_report_{assessment_id}.pdf"'
        return response
    except Exception as e:
        logger.exception("Error serving report file")
        return JsonResponse({'error': str(e)}, status=500)

def verify_token(token):
    """Verify JWT token using rest_framework_simplejwt"""
    try:
        # Use AccessToken to validate and decode
        validated_token = AccessToken(token)
        
        # Get user_id from token
        user_id = validated_token.get('user_id')
        if not user_id:
            return False, "Invalid token: 'user_id' not found"
            
        return True, validated_token.payload
    except TokenError as e:
        return False, str(e)
    except Exception as e:
        logger.exception("Token verification error")
        return False, str(e)

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Handle user registration through SSO service"""
    try:
        data = {
            'email': request.POST['email'],
            'password': request.POST['password']
        }
        
        # Try to register with SSO service
        response = requests.post(
            f"{settings.SSO_BASE_URL}register/",
            json=data,
            timeout=5
        )
        
        if response.status_code == 400:
            # Check if error is due to existing email
            error_data = response.json()
            if 'email' in error_data and 'already exists' in str(error_data['email']).lower():
                # Email exists in SSO, try to login instead
                login_response = requests.post(
                    f"{settings.SSO_BASE_URL}login/",
                    json=data,
                    timeout=5
                )
                
                if login_response.status_code != 200:
                    return JsonResponse({'error': 'Invalid credentials'}, status=400)
                    
                tokens = login_response.json()
                
                # If MFA is required, return that to the client
                if tokens.get('mfa_required'):
                    return JsonResponse(tokens)
                
                # Verify the access token
                is_valid, token_data = verify_token(tokens['access'])
                if not is_valid:
                    return JsonResponse({'error': f'Token verification failed: {token_data}'}, status=400)
                
                # Create local user profile if it doesn't exist
                try:
                    user = User.objects.get(username=token_data['user_id'])
                except User.DoesNotExist:
                    # Create user locally
                    user = User.objects.create(
                        username=token_data['user_id'],
                        email=request.POST['email']
                    )
                
                # Create or update profile
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'full_name': request.POST['full_name'],
                        'phone_number': request.POST['phone']
                    }
                )
                
                # Associate pending assessment if exists
                pending_assessment_id = request.session.get('pending_assessment_id')
                if pending_assessment_id:
                    try:
                        assessment = BusinessAssessment.objects.get(id=pending_assessment_id)
                        user.profile.assessments.add(assessment)
                        del request.session['pending_assessment_id']
                    except BusinessAssessment.DoesNotExist:
                        pass
                
                return JsonResponse(tokens)
            else:
                # Other registration error
                return JsonResponse({'error': error_data}, status=400)
        
        elif response.status_code != 201:
            return JsonResponse({'error': 'Registration failed'}, status=400)
            
        # Get tokens from successful registration
        tokens = response.json()
        
        # Verify the access token
        is_valid, token_data = verify_token(tokens['access'])
        if not is_valid:
            return JsonResponse({'error': f'Token verification failed: {token_data}'}, status=400)
        
        # Create user profile
        try:
            user = User.objects.get(username=token_data['user_id'])
        except User.DoesNotExist:
            user = User.objects.create(
                username=token_data['user_id'],
                email=request.POST['email']
            )
            
        UserProfile.objects.create(
            user=user,
            full_name=request.POST['full_name'],
            phone_number=request.POST['phone']
        )
        
        # Associate pending assessment if exists
        pending_assessment_id = request.session.get('pending_assessment_id')
        if pending_assessment_id:
            try:
                assessment = BusinessAssessment.objects.get(id=pending_assessment_id)
                user.profile.assessments.add(assessment)
                del request.session['pending_assessment_id']
            except BusinessAssessment.DoesNotExist:
                pass
        
        return JsonResponse(tokens)
        
    except Exception as e:
        logger.exception("Registration error")
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login(request):
    """Handle user login through SSO service"""
    if request.method == 'GET':
        # Show login form
        next_url = request.GET.get('next', '')
        return render(request, 'readiness/login.html', {'next': next_url})
        
    # Handle POST request for login
    try:
        # Parse JSON data from request body
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        # Login with SSO service
        response = requests.post(
            f"{settings.SSO_BASE_URL}login/",
            json={
                'email': email,
                'password': password
            },
            timeout=5
        )
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
            
        # Get tokens from response
        tokens = response.json()
        
        # Check if MFA is required
        if tokens.get('mfa_required'):
            return JsonResponse({'mfa_required': True, 'message': tokens['message']})
            
        # Verify the access token
        is_valid, token_data = verify_token(tokens['access'])
        if not is_valid:
            return JsonResponse({'error': f'Token verification failed: {token_data}'}, status=400)
        
        # Store refresh token in session
        request.session['refresh_token'] = tokens['refresh']
        
        # Create local user if doesn't exist
        try:
            user = User.objects.get(username=token_data['user_id'])
        except User.DoesNotExist:
            user = User.objects.create(
                username=token_data['user_id'],
                email=email
            )
        
        # Get or create profile
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(
                user=user,
                full_name=token_data.get('full_name', email.split('@')[0]),
                phone_number=''
            )
        
        # Associate pending assessment if exists
        pending_assessment_id = request.session.get('pending_assessment_id')
        if pending_assessment_id:
            try:
                assessment = BusinessAssessment.objects.get(id=pending_assessment_id)
                profile.assessments.add(assessment)
                del request.session['pending_assessment_id']
            except BusinessAssessment.DoesNotExist:
                pass
            
        # Get the next URL from the request or default to dashboard
        next_url = data.get('next') or reverse('readiness:user_dashboard')
        
        # Log the user in
        from django.contrib.auth import login as auth_login
        auth_login(request, user)
        
        return JsonResponse({
            'success': True,
            'redirect_url': next_url,
            **tokens
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("Login error")
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
@login_required
def user_dashboard(request):
    """Render user dashboard"""
    assessments = request.user.profile.assessments.all().order_by('-created_at')
    latest_assessment = assessments.first() if assessments.exists() else None
    return render(request, 'readiness/user_dashboard.html', {
        'assessments': assessments,
        'latest_assessment': latest_assessment
    })

@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    """Handle user logout through SSO service"""
    try:
        refresh_token = request.session.get('refresh_token')
        
        # Even if SSO logout fails, we should still logout locally
        try:
            if refresh_token:
                # Logout with SSO service
                response = requests.post(
                    f"{settings.SSO_BASE_URL}logout/",
                    json={'refresh': refresh_token},
                    timeout=5
                )
                # Log but don't fail if SSO logout fails
                if response.status_code != 205:
                    logger.warning(f"SSO logout failed with status {response.status_code}")
        except Exception as e:
            logger.warning(f"SSO logout failed: {str(e)}")
        
        # Clear Django session and logout
        from django.contrib.auth import logout as auth_logout
        auth_logout(request)
        
        # Clear session data
        request.session.flush()
            
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
        
    except Exception as e:
        logger.exception("Logout error")
        return JsonResponse({'error': str(e)}, status=400) 