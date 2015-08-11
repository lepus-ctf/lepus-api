# encoding=utf-8
from rest_framework import generics, permissions, viewsets, filters, status
from django.contrib.auth import authenticate, login
from rest_framework.response import Response

from .serializers import TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, FileSerializer, \
    AnswerSerializer, NoticeSerializer



# TODO:正しくAuthを実装する

class AuthView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            return Response(UserSerializer(request.user).data)

        return Response({"error": "未ログインです"}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        name = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=name, password=password)

        if user is not None:
            login(request, user)
            serialized_user = UserSerializer(request.user)
            return Response(serialized_user.data)

        return Response({"error": "無効なID,パスワードです"}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all() # FIXME:Questionが存在しないCategoryを隠す
    permission_classes = (permissions.IsAuthenticated,)


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_public=True)
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category',)


class FileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FileSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_public=True, question__is_public=True)
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('question',)

    def download(self):
        # TODO:Implement
        pass


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)



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
    queryset = serializer_class.Meta.model.objects.filter(is_public=True)
    permission_classes = (permissions.AllowAny,)

# TODO:AttackPointのAPIを開発する
