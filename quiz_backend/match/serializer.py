from rest_framework import serializers
from match.models import Match


class MatchSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Match
        fields = '__all__'

