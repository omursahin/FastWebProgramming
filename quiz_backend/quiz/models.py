from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer_1 = models.CharField(max_length=255)
    answer_2 = models.CharField(max_length=255)
    answer_3 = models.CharField(max_length=255)
    answer_4 = models.CharField(max_length=255)
    correct_answer = models.IntegerField()

    class Meta:
        verbose_name_plural = 'quizes'

    def __str__(self):
        return str(self.id)