from django.db import models

# Create your models here.
from match.models import Match
from quiz.models import Quiz


class QuizSet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.IntegerField(null=True)
    is_correct = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = 'quiz_sets'

    def __str__(self):
        return str(self.id)