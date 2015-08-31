import datetime
from django.utils.timezone import utc

from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from lepus.models import Config


class TimeException(APIException):
    status_code = 503

    def __init__(self, message="", error=""):
        self.detail = {"message": message, "errors": [error, ]}
        super(APIException, self).__init__(self.detail)


class IsClosed(BasePermission):
    def has_permission(self, request, view):
        end = Config.get(key='end_at')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        if end:
            if end < now:
                raise TimeException(message="CTF closed.", error="CLOSED")

        return True


class IsStarted(BasePermission):
    def has_permission(self, request, view):
        start = Config.get(key='start_at')
        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        if start:
            if start > now:
                raise TimeException(message="CTF isn't started.", error="NOT_STARTED")

        return True
