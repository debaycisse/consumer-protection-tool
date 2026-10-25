from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler


def general_exception(exception, context):
    """
    To ensure consistency in error message
    structure for all resources
    """

    # To handle only resource not found exception
    if isinstance(exception, ObjectDoesNotExist):
        kwargs = context.get("kwargs", {})
        if kwargs:
            field_value = next(iter(kwargs.values()))
        else:
            field_value = "unknown"

        resource_name = context.get("view").queryset.model.__name__
        if resource_name.endswith("s"):
            resource_name = resource_name[:-1]

        error_response_data = {
            "details": f"{resource_name} not found",
            "description": f"{resource_name} with id {field_value} \
                does not exist in our database",
            "error_code": "RESOURCE_DOES_NOT_EXIST",
        }

        return Response(
            error_response_data, status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exception, AuthenticationFailed):
        error_response_data = {
            "details": "invalid username or password",
            "description": "either username or password was incorrect",
            "error_code": "INVALID_CREDENTIALS",
        }

        return Response(
            error_response_data, status=status.HTTP_400_BAD_REQUEST
        )

    # To pass all other exception types to DRF
    return exception_handler(exc=exception, context=context)
