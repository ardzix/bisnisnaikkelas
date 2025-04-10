from django.contrib import admin
from .models import ReadinessAssessment, ReadinessQuestion, ReadinessAnswer, BusinessAssessment


@admin.register(ReadinessQuestion)
class ReadinessQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'weight', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question_text',)


@admin.register(ReadinessAssessment)
class ReadinessAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'score', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('score', 'created_at', 'updated_at')


@admin.register(ReadinessAnswer)
class ReadinessAnswerAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'question', 'answer', 'created_at')
    list_filter = ('question__category', 'created_at')
    search_fields = ('assessment__user__email', 'question__question_text')
    readonly_fields = ('created_at',)


@admin.register(BusinessAssessment)
class BusinessAssessmentAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_type', 'year_started', 'employee_count', 
                   'total_score', 'business_level', 'created_at')
    list_filter = ('business_type', 'business_level', 'created_at')
    search_fields = ('business_name',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'report_ready', 'report_pdf',
                      'digital_score', 'financial_score', 'legal_score', 'operational_score',
                      'strategy_score', 'compliance_score', 'technology_score', 'market_score',
                      'process_score', 'total_score', 'business_level', 'recommendations')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'business_name', 'business_type', 'year_started', 'employee_count', 
                      'annual_revenue', 'business_goals', 'interested_in_mentoring')
        }),
        ('Financial Information', {
            'fields': ('has_financial_records', 'has_invoice_system', 'uses_financial_software',
                      'has_cashflow_forecast', 'has_tax_calculation_practice')
        }),
        ('Digital Presence', {
            'fields': ('has_website', 'has_online_store', 'has_social_media',
                      'is_social_media_active', 'uses_digital_ads', 'uses_crm_or_marketing_tools')
        }),
        ('Legal Documentation', {
            'fields': ('has_npwp', 'has_business_license', 'has_profit_loss_statement',
                      'has_balance_sheet', 'has_contract_templates', 'registered_with_government_platforms')
        }),
        ('Operational', {
            'fields': ('has_sop_documentation', 'has_team_structure')
        }),
        ('Strategy', {
            'fields': ('has_vision_and_mission', 'has_business_plan', 'has_defined_target_market',
                      'has_unique_value_proposition')
        }),
        ('Risk & Compliance', {
            'fields': ('has_data_backup', 'has_been_audited', 'has_third_party_contracts',
                      'has_tax_risk_management', 'has_internal_controls')
        }),
        ('Technology', {
            'fields': ('uses_inventory_software', 'can_operate_remotely',
                      'uses_automation_or_integration', 'has_internal_dashboard_or_kpi_system')
        }),
        ('Market Access', {
            'fields': ('sells_nationally_or_internationally', 'attends_trade_expos',
                      'has_reseller_or_distributor', 'has_partnership_program')
        }),
        ('Process Maturity', {
            'fields': ('has_payroll_system', 'has_quality_control_process',
                      'has_employee_handbook_or_sop', 'has_formal_onboarding')
        }),
        ('Assessment Results', {
            'fields': ('digital_score', 'financial_score', 'legal_score', 'operational_score',
                      'strategy_score', 'compliance_score', 'technology_score', 'market_score',
                      'process_score', 'total_score', 'business_level', 'recommendations')
        }),
        ('Report Information', {
            'fields': ('report_pdf', 'report_ready', 'created_at', 'updated_at')
        }),
    ) 