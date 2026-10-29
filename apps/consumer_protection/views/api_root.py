from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .resource_endpoints import get_resource_endpoints


class APIViewRoot(APIView):

    def get(self, request, format=None):

        response_data = {
            "endpoints": get_resource_endpoints(request, format)
        }

        return Response(response_data, status=status.HTTP_200_OK)
