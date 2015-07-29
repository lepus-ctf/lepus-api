# encoding=utf-8
from rest_framework import generics, permissions
from .serializers import TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, FileSerializer, \
    AnswerSerializer, NoticeSerializer


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


class QuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.IsAuthenticated


class CategoryView(generics.ListAPIView):
    serializer_class = CategorySerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.IsAuthenticated


class FileView(generics.ListAPIView):
    serializer_class = FileSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.IsAuthenticated


class AnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.IsAuthenticated


class NoticeView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = permissions.AllowAny


# TODO:AttackPointのAPIを開発する
