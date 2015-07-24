# encoding=utf-8
from rest_framework import generics, permissions
from .serializers import TeamSerializer, UserSerializer


class TeamListView(generics.ListAPIView):
    serializer_class = TeamSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.AllowAny


class AuthView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.IsAuthenticated


