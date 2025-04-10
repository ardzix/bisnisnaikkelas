from rest_framework import serializers
from .models import ReadinessAssessment, ReadinessQuestion, ReadinessAnswer


class ReadinessQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadinessQuestion
        fields = ['id', 'question_text', 'category', 'weight', 'is_active']


class ReadinessAnswerSerializer(serializers.ModelSerializer):
    question = ReadinessQuestionSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ReadinessAnswer
        fields = ['id', 'question', 'question_id', 'answer', 'created_at']
        read_only_fields = ['created_at']


class ReadinessAssessmentSerializer(serializers.ModelSerializer):
    answers = ReadinessAnswerSerializer(many=True, read_only=True)
    score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = ReadinessAssessment
        fields = ['id', 'user', 'status', 'score', 'answers', 'created_at', 'updated_at']
        read_only_fields = ['user', 'score', 'created_at', 'updated_at'] 