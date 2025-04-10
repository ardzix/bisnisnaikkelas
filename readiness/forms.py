from django import forms
from .models import ReadinessAssessment, ReadinessAnswer


class ReadinessAssessmentForm(forms.ModelForm):
    class Meta:
        model = ReadinessAssessment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ReadinessAnswerForm(forms.ModelForm):
    class Meta:
        model = ReadinessAnswer
        fields = ['answer']
        widgets = {
            'answer': forms.Select(attrs={'class': 'form-control'}),
        }


class ReadinessAnswerFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = ReadinessAnswer.objects.none() 