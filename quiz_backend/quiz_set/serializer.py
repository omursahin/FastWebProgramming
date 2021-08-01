from rest_framework import serializers

from match.serializer import MatchSerializer
from quiz.serializer import QuizSerializer
from quiz_set.models import QuizSet


class QuizSetSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()

    class Meta:
        model = QuizSet
        fields = '__all__'
