import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class BusinessAssessment(models.Model):
    BUSINESS_TYPES = [
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('service', 'Service'),
        ('food', 'Food & Beverage'),
        ('other', 'Other'),
    ]
    
    BUSINESS_LEVELS = [
        ('micro', 'Micro'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic Information
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES)
    year_started = models.IntegerField()
    employee_count = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Financial Information
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    has_financial_records = models.BooleanField(default=False)
    has_invoice_system = models.BooleanField(default=False)
    uses_financial_software = models.BooleanField(default=False)
    has_cashflow_forecast = models.BooleanField(default=False)
    has_tax_calculation_practice = models.BooleanField(default=False)
    
    # Digital Presence
    has_website = models.BooleanField(default=False)
    has_online_store = models.BooleanField(default=False)
    has_social_media = models.BooleanField(default=False)
    is_social_media_active = models.BooleanField(default=False)
    uses_digital_ads = models.BooleanField(default=False)
    uses_crm_or_marketing_tools = models.BooleanField(default=False)
    
    # Legal Documentation
    has_npwp = models.BooleanField(default=False)
    has_business_license = models.BooleanField(default=False)
    has_profit_loss_statement = models.BooleanField(default=False)
    has_balance_sheet = models.BooleanField(default=False)
    has_contract_templates = models.BooleanField(default=False)
    registered_with_government_platforms = models.BooleanField(default=False)
    
    # Operational
    has_sop_documentation = models.BooleanField(default=False)
    has_team_structure = models.BooleanField(default=False)
    
    # Strategy
    has_vision_and_mission = models.BooleanField(default=False)
    has_business_plan = models.BooleanField(default=False)
    has_defined_target_market = models.BooleanField(default=False)
    has_unique_value_proposition = models.BooleanField(default=False)
    
    # Risk & Compliance
    has_data_backup = models.BooleanField(default=False)
    has_been_audited = models.BooleanField(default=False)
    has_third_party_contracts = models.BooleanField(default=False)
    has_tax_risk_management = models.BooleanField(default=False)
    has_internal_controls = models.BooleanField(default=False)
    
    # Technology
    uses_inventory_software = models.BooleanField(default=False)
    can_operate_remotely = models.BooleanField(default=False)
    uses_automation_or_integration = models.BooleanField(default=False)
    has_internal_dashboard_or_kpi_system = models.BooleanField(default=False)
    
    # Market Access
    sells_nationally_or_internationally = models.BooleanField(default=False)
    attends_trade_expos = models.BooleanField(default=False)
    has_reseller_or_distributor = models.BooleanField(default=False)
    has_partnership_program = models.BooleanField(default=False)
    
    # Process Maturity
    has_payroll_system = models.BooleanField(default=False)
    has_quality_control_process = models.BooleanField(default=False)
    has_employee_handbook_or_sop = models.BooleanField(default=False)
    has_formal_onboarding = models.BooleanField(default=False)
    
    # Business Goals
    business_goals = models.TextField()
    interested_in_mentoring = models.BooleanField(default=False)
    
    # Assessment Results
    # These fields are kept for backward compatibility
    # The actual scores are now calculated dynamically based on business level
    digital_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    financial_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    legal_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    operational_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    strategy_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    compliance_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    technology_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    market_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    process_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    total_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    business_level = models.CharField(
        max_length=10,
        choices=BUSINESS_LEVELS,
        null=True,
        blank=True
    )
    recommendations = models.JSONField(null=True, blank=True)
    
    # PDF Report
    report_pdf = models.FileField(upload_to='reports/', null=True, blank=True)
    report_ready = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.business_name} - {self.created_at.strftime('%Y-%m-%d')}"

class ReadinessQuestion(models.Model):
    question_text = models.TextField()
    category = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'id']

    def __str__(self):
        return f"{self.category} - {self.question_text[:50]}..."

class ReadinessAssessment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Assessment {self.id} - {self.user.email}"

class ReadinessAnswer(models.Model):
    ANSWER_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('partial', 'Partial'),
    ]

    assessment = models.ForeignKey(ReadinessAssessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ReadinessQuestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10, choices=ANSWER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['question__category', 'question__id']
        unique_together = ('assessment', 'question')

    def __str__(self):
        return f"{self.assessment.id} - {self.question.question_text[:50]}..."

    def is_dirty(self):
        """
        Check if the answer has been modified since creation.
        """
        if not self.pk:  # New instance
            return True
        return False 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    assessments = models.ManyToManyField('BusinessAssessment', related_name='users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})" 