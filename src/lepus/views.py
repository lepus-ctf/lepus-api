# encoding=utf-8
from rest_framework.decorators import detail_route, list_route
from rest_framework import generics, permissions, viewsets, filters, status, mixins
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response

from .serializers import AuthSerializer, TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, FileSerializer, \
    AnswerSerializer, NoticeSerializer

from .models import *
from django.http import HttpResponse
import mimetypes

class AuthViewSet(viewsets.ViewSet):
    serializer_class = AuthSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response(UserSerializer(request.user).data)

        return Response({"error": "未ログインです"}, status=status.HTTP_401_UNAUTHORIZED)


    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            login(request, serializer.get_user())
            return self.list(request, *args, **kwargs)

    @list_route(methods=["post"])
    def logout(self, request, *args, **kwargs):
        logout(request)
        return self.list(request, *args, **kwargs)

class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(id=-1)

    def get_queryset(self):
        return User.objects.filter(team=self.request.user.team)



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

    def download(self, **kwargs):
        file_id = kwargs['file_id']
        file = File.objects.get(id=file_id)
        if file is not None:
            mime = mimetypes.guess_type(file.url)
            file_bin = open(file.url,'rb').read()
            response = HttpResponse(file_bin, content_type=mime)
            response['Content-Disposition'] = 'filename=%s' % file.name
            return response
        else:
            return "" #FIXME


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.IsAuthenticated,)



class AnswerViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.filter(id=-1)
    permission_classes = (permissions.IsAuthenticated,)


class NoticeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NoticeSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_public=True)
    permission_classes = (permissions.AllowAny,)

# TODO:AttackPointのAPIを開発する
