# encoding=utf-8
from rest_framework import generics
from .serializers import TeamSerializer

class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    model = serializer_class.Meta.model
