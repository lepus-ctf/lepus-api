# encoding=utf-8
import mimetypes

from rest_framework.decorators import list_route
from rest_framework import permissions, viewsets, filters, status, mixins
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from django.http import HttpResponse

from lepus.permissions import IsClosed, IsStarted
from .serializers import AuthSerializer, TeamSerializer, UserSerializer, QuestionSerializer, CategorySerializer, \
    AnswerSerializer, NoticeSerializer, ConfigSerializer
from .models import *


class DynamicDepthMixins(object):
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super(DynamicDepthMixins, self).get_serializer_class()
        serializer_class.Meta.depth = 0

        if self.request.method == "GET":
            include = self.request.GET.get("include", "").lower()
            if include in ("1", "true"):
                serializer_class.Meta.depth = 1

        return serializer_class


class AuthViewSet(viewsets.ViewSet):
    serializer_class = AuthSerializer

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return Response(UserSerializer(request.user).data)

        return Response({"message": "Authentication is required.", "errors": [{"error": "unauthorized"}]},
                        status=status.HTTP_401_UNAUTHORIZED)

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
                  DynamicDepthMixins,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(id=-1)
    permission_classes = ()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return User.objects.filter(team=self.request.user.team)
        return self.queryset


class CategoryViewSet(DynamicDepthMixins, viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()  # FIXME:Questionが存在しないCategoryを隠す
    permission_classes = (permissions.IsAuthenticated,)


class QuestionViewSet(DynamicDepthMixins, viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    queryset = serializer_class.Meta.model.objects.public().prefetch_related("flag_set", "file_set")
    permission_classes = (permissions.IsAuthenticated, IsStarted)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('category',)


def download_file(request, file_id, filename=""):
    f = get_object_or_404(File.objects.public(), id=file_id)
    if filename != f.name:
        raise Http404
    mime_type = mimetypes.guess_type(f.file.name)[0]
    response = HttpResponse(content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % f.name
    response.write(f.file.read())
    return response


class TeamViewSet(DynamicDepthMixins, viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamSerializer
    queryset = serializer_class.Meta.model.objects.prefetch_related("answer_set", "attackpoint_set", "answer_set__flag", "answer_set__flag__question")
    permission_classes = (permissions.IsAuthenticated,)


class AnswerViewSet(mixins.CreateModelMixin,
                    DynamicDepthMixins,
                    viewsets.GenericViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.filter(id=-1)
    permission_classes = (permissions.IsAuthenticated, IsStarted, IsClosed)


class NoticeViewSet(DynamicDepthMixins, viewsets.ReadOnlyModelViewSet):
    serializer_class = NoticeSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_public=True)
    permission_classes = (permissions.AllowAny,)


class ConfigViewSet(DynamicDepthMixins, viewsets.ReadOnlyModelViewSet):
    lookup_field = "key"
    serializer_class = ConfigSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (permissions.AllowAny,)


# TODO:AttackPointのAPIを開発する
