# encoding=utf-8
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from rest_framework.response import Response

from lepus.serializers import ValidationErrorDetail

def exception_handler(exc, context):
    if isinstance(exc, exceptions.ValidationError):
        errors = []
        message = "Validation failed."

        for field, field_errors in exc.detail.items():

            if field == "non_field_errors":
                field = None

            for error in field_errors:

                if isinstance(error, ValidationErrorDetail):
                    message = error.message
                    error = {"error": error.error}
                else:
                    error = {"error": error}

                if field:
                    error["field"] = field
                errors.append(error)

        data = {
            "message": message,
            "errors": errors
        }
        return Response(data, status=422)

    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, list):
            errors = [{"error": e} for e in exc.detail]
            data = {"message": "API exception occured.", "errors": errors}
        elif isinstance(exc.detail, dict):
            message = exc.detail.get("message", "API exception occured.")
            errors = [{"error": e} for e in exc.detail.get("errors", [])]
            data = {'message': message, "errors": errors}
        else:
            data = {'message': exc.detail, "errors":[]}

        set_rollback()
        return Response(data, status=exc.status_code)

    elif isinstance(exc, Http404):
        data = {
            "message":"Not found.",
            "errors":[
                {"error":"not_found"}
            ]
        }
        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        data = {
            "message":"Permision denied.",
            "errors":[
                {"error":"permission_denied"}
            ]
        }
        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    # Note: Unhandled exceptions will raise a 500 error.
    return None
