# encoding=utf-8
from rest_framework.routers import DefaultRouter
from rest_framework import permissions, viewsets, mixins
from lepus.admin.serializers import AdminUserSerializer, AdminTeamSerilaizer, AdminCategorySerializer, AdminQuestionSerializer, AdminFlagSerializer, AdminAnswerSerializer, AdminNoticeSerializer
from lepus.models import *
from lepus.views import DynamicDepthMixins

router = DefaultRouter()

class AdminUserViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    queryset = User.objects.filter(team__isnull=False)
    permission_classes = (permissions.IsAdminUser,)

router.register("users", AdminUserViewSet)


class AdminTeamViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminTeamSerilaizer
    queryset = Team.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("teams", AdminTeamViewSet)


class AdminCategoryViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminCategorySerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("categories", AdminCategoryViewSet)


class AdminQuestionViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminQuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("questions", AdminQuestionViewSet)


class AdminFlagViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminFlagSerializer
    queryset = Flag.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("flags", AdminFlagViewSet)


class AdminAnswerViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         DynamicDepthMixins,
                         viewsets.GenericViewSet):
    serializer_class = AdminAnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("answers", AdminAnswerViewSet)


class AdminNoticeViewSet(DynamicDepthMixins, viewsets.ModelViewSet):
    serializer_class = AdminNoticeSerializer
    queryset = Notice.objects.all()
    permission_classes = (permissions.IsAdminUser,)

router.register("notices", AdminNoticeViewSet)
