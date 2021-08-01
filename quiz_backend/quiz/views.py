from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from quiz.models import Quiz
from quiz.serializer import QuizSerializer


class QuizList(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuizSerializer
        if self.request.method == 'POST':
            return QuizSerializer
        return QuizSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(owner=self.request.user)

    queryset = Quiz.objects.all()


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QuizSerializer
        if self.request.method == 'POST':
            return QuizSerializer

        return QuizSerializer

    queryset = Quiz.objects.all()