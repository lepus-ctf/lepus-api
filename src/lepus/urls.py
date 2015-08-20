# encoding=utf-8

"""lepus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from lepus.views import AuthViewSet, UserViewSet, QuestionViewSet, TeamViewSet, CategoryViewSet, FileViewSet, \
    NoticeViewSet, AnswerViewSet, download_file
from lepus.admin.views import router as admin_router

router = DefaultRouter()
router.register(r'auth', AuthViewSet, base_name="auth")
router.register(r'users', UserViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answer', AnswerViewSet, base_name="answers")
router.register(r'teams', TeamViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'files', FileViewSet)
router.register(r'notices', NoticeViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^files/(\d+)/(.+)$', download_file, name="download_file"),
    url(r'adminapi/', include(admin_router.urls, namespace='adminapi')),
    url(r'api/', include(router.urls, namespace='api'))
]
