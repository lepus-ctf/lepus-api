# encoding=utf-8

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.routers import DefaultRouter

from lepus.models import *
from lepus.internal.serializers import AttackPointSerializer, UserSerializer

router = DefaultRouter()

class AttackPointViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = AttackPointSerializer
    queryset = AttackPoint.objects.all()

router.register("attackpoints", AttackPointViewSet)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        ip = self.request.GET.get("ip")
        if ip:
            queryset = User.objects.by_ip(ip)
        else:
            queryset = self.queryset
        return queryset


router.register("users", UserViewSet)
