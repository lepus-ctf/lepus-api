# encoding=utf-8

from lepus.models import UserConnection

class UserConnectionMiddleware(object):
    def process_request(self, request):
        user = request.user
        ip = request.META.get("HTTP_X_REAL_IP")
        if not ip:
            ip = request.META.get("REMOTE_ADDR")

        if user.is_authenticated() and ip:
            UserConnection.update(user, ip)
