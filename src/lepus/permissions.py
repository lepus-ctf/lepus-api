from datetime import datetime

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
        end = Config.get(key='end_date')
        now = datetime.now()

        if end:
            if end.value < now:
                raise TimeException(message="CTF closed.", error="CLOSED")

        return True


class IsStarted(BasePermission):
    def has_permission(self, request, view):
        start = Config.get(key='start_date')
        now = datetime.now()

        if start:
            if start.value > now:
                raise TimeException(message="CTF isn't started.", error="NOT_STARTED")

        return True
