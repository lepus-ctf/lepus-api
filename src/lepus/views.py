# encoding=utf-8
from rest_framework import generics, permissions, viewsets, filters, status
from django.contrib.auth import authenticate, login
from rest_framework.response import Response

from .serializers import TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, FileSerializer, \
    AnswerSerializer, NoticeSerializer



# TODO:正しくAuthを実装する

class AuthView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        name = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=name, password=password)

        if user is not None:
            login(request, user)
            serialized_user = UserSerializer(request.user)
            return Response(serialized_user.data)

        return Response({"error": "無効なID,パスワードです"}, status=status.HTTP_401_UNAUTHORIZED)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category',)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class FileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FileSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('question',)


class AnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


"""
    def create(self, request, *args, **kwargs):
        answer_serializer = AnswerSerializer(question=request.data['question'], answer=request.data['answer'],
                                             user=request.user.id)
"""


class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NoticeSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.AllowAny,)

# TODO:AttackPointのAPIを開発する
