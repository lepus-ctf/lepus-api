# encoding=utf-8
from rest_framework import generics, permissions, viewsets, filters
from .serializers import TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, FileSerializer, \
    AnswerSerializer, NoticeSerializer


# TODO:正しくAuthを実装する
class AuthView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


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
