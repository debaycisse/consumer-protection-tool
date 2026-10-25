from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.leaderboards_serializer import LeaderboardSerializer
from apps.consumer_protection.models.leaderboards import Leaderboard
from apps.consumer_protection.views.utils import CommonViewAttributes


class LeaderboardPermissions:
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]


class LeaderboardListCreateView(
    LeaderboardPermissions, CommonViewAttributes, APIView
):
    """
    View to process list and create requests
    for leaderboard resource

    Requires an authentication token
    """

    def get(self, request, format=None):
        leaderboards = Leaderboard.objects.select_related("producer_id")

        leaderboard_serializer = LeaderboardSerializer(
            leaderboards, many=True
        )

        response_data = {"data": leaderboard_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_leaderboard = Leaderboard.objects.create(**request_data)

        self.check_object_permissions(request, new_leaderboard)

        serializer = LeaderboardSerializer(data=new_leaderboard)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {"data": serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class LeaderboardRetrieveUpdateDestroyView(
    LeaderboardPermissions, CommonViewAttributes, APIView
):
    """
    View to process retrieve, update, and delete requests
    for a leaderboard resource

    Requires an authentication token
    """

    def get_object(self, leaderboard_id=None):
        return Leaderboard.objects.select_related("producer_id").get(
            leaderboard_id=leaderboard_id
        )

    def get(self, request, leaderboard_id=None, format=None):
        leaderboard = self.get_object(leaderboard_id)

        leaderboard_serializer = LeaderboardSerializer(leaderboard)

        response_data = {"data": leaderboard_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, leaderboard_id=None, format=None):
        leaderboard = self.get_object(leaderboard_id)

        self.check_object_permissions(request, leaderboard)

        request_data = request.data

        leaderboard_serializer = LeaderboardSerializer(
            leaderboard, data=request_data, partial=True
        )
        leaderboard_serializer.is_valid(raise_exception=True)
        leaderboard_serializer.save()

        response_data = {"data": leaderboard_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, leaderboard_id=None, format=None):
        leaderboard = self.get_object(leaderboard_id)

        self.check_object_permissions(request, leaderboard)

        leaderboard.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
