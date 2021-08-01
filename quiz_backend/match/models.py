from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Match(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_defeat = models.BooleanField(default=False)
    is_victory = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'matches'

    def __str__(self):
        return str(self.id)