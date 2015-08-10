#! encoding=utf8

from rest_framework import serializers, status


class AuthenticationError(serializers.ValidationError):
    status_code = status.HTTP_401_UNAUTHORIZED
