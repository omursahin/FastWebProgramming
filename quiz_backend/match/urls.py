from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from match import views

urlpatterns = [
    path('', views.MatchList.as_view()),
    path('ongoing/', views.MatchOngoing.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
