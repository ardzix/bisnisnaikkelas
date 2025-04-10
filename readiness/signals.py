from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import ReadinessAssessment, ReadinessQuestion, ReadinessAnswer
from .tasks import calculate_readiness_score


@receiver(post_save, sender=ReadinessAnswer)
def answer_post_save(sender, instance, created, **kwargs):
    """
    Signal handler to recalculate readiness score when an answer is saved.
    """
    if created or instance.is_dirty():
        calculate_readiness_score.delay(instance.assessment.id)


@receiver(pre_save, sender=ReadinessAssessment)
def assessment_pre_save(sender, instance, **kwargs):
    """
    Signal handler to set default values before saving an assessment.
    """
    if not instance.pk:  # Only for new instances
        instance.status = 'draft' 