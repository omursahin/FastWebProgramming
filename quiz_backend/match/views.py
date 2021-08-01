import random

from django.db import transaction

# Create your views here.
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from match.models import Match
from match.serializer import MatchSerializer
from quiz.models import Quiz
from quiz_set.models import QuizSet
from quiz_set.serializer import QuizSetSerializer


class MatchList(generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MatchSerializer
        if self.request.method == 'POST':
            return MatchSerializer
        return MatchSerializer

    def post(self, request, *args, **kwargs):
        current_match = Match.objects.filter(Q(user=request.user) & Q(is_defeat=False) & Q(is_victory=False))
        if current_match:
            serialized_data = MatchSerializer(current_match, many=True)
            return Response(serialized_data.data, status=200)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        with transaction.atomic():
            saved_instance = serializer.save(user=self.request.user)
            quiz_id_list = Quiz.objects.values_list('id', flat=True)
            random_quiz_id_list = random.sample(list(quiz_id_list), 3)
            query_set = Quiz.objects.filter(id__in=random_quiz_id_list)
            for q in query_set:
                new_quiz = QuizSet(match_id=saved_instance.id, quiz=q)
                new_quiz.save()
    queryset = Match.objects.all()


class MatchOngoing(generics.ListCreateAPIView):
    serializer_class = QuizSetSerializer
    queryset = QuizSet.objects.all()

    def list(self, request, *args, **kwargs):
        current_match = Match.objects.filter(Q(user=request.user) & Q(is_defeat=False) & Q(is_victory=False))
        if current_match:
            current_quiz = QuizSet.objects.filter(match__in=current_match).filter(answer=None).first()
            serializer = QuizSetSerializer(current_quiz)
            return Response(serializer.data)
        else:
            return Response(data={'info': 'Devam eden oyun bulunmamaktadir'})

    def post(self, request, *args, **kwargs):
        try:
            answer_id = self.request.data['answer_id']
        except KeyError:
            current_match = Match.objects.filter(Q(user=request.user) & Q(is_defeat=False) & Q(is_victory=False)).first()
            if current_match:
                current_quiz = QuizSet.objects.filter(match=current_match).filter(answer=None).first()
                serializer = QuizSetSerializer(current_quiz)
                return Response(serializer.data)
            else:
                return Response(data={'info': 'Devam eden oyun bulunmamaktadir'})

        with transaction.atomic():
            current_match = Match.objects.filter(Q(user=request.user) & Q(is_defeat=False) & Q(is_victory=False)).first()
            if current_match:
                current_quiz = QuizSet.objects.filter(match=current_match).filter(answer=None).first()
                is_correct = current_quiz.quiz.correct_answer == answer_id
                current_quiz.answer = answer_id
                current_quiz.is_correct = is_correct
                current_quiz.save()
                if not is_correct:
                    current_match.is_defeat = True
                    current_match.save()
                    return Response(data={'info': 'Kaybettin'})
                else: #Eger sirada yeni bir soru yoksa oyun kazanilmistir
                    current_quiz = QuizSet.objects.filter(match=current_match).filter(answer=None).first()
                    if not current_quiz:
                        current_match.is_victory = True
                        current_match.save()
                        return Response(data={'info': 'Kazandın'})

                    else:
                        serializer = QuizSetSerializer(current_quiz)
                        return Response(serializer.data)
            else:
                return Response(data={'info': 'Devam eden oyun bulunmamaktadir'})
