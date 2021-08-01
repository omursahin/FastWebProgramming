from rest_framework import serializers
from quiz.models import Quiz


class QuizSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Quiz
        exclude = ['correct_answer']

