from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.consumer_protection.views.utils import CommonViewAttributes
from apps.consumer_protection.models.comments import Comments
from apps.consumer_protection.serializers.comments_serializer import (
    CommentSerializer,
)
from apps.consumer_protection.permissions.owner_permission import (
    IsCommentOwner,
)


class CommentListCreateView(CommonViewAttributes, APIView):
    """
    View to list all comments and create a new comment

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        comment_objects = Comments.objects.select_related(
            "feedback_id", "commenter_id"
        )
        comments_serializer = CommentSerializer(
            comment_objects, many=True
        )

        response_data = {"data": comments_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_comment_object = Comments.objects.create(**request_data)

        comment_serializer = CommentSerializer(data=new_comment_object)
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save(commenter_id=request.user)

        response_data = {"data": comment_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class CommentRetrieveUpdateDestroyView(CommonViewAttributes, APIView):
    """
    View to handle getting, partially updating, and
    deleting a single comment resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwner]

    def get_object(self, comment_id):
        return Comments.objects.select_related(
            "commenter_id", "feedback_id"
        ).get(comment_id=comment_id)

    def get(self, request, comment_id=None, format=None):
        comment = self.get_object(comment_id=comment_id)
        serializer = CommentSerializer(comment)

        return Response(
            {"data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, comment_id=None, format=None):
        comment_object = self.get_object(comment_id=comment_id)
        request_data = request.data.get("body", comment_object.body)

        # to confirm the change is being made by the commenter
        self.check_object_permissions(request, comment_object)

        comment_serializer = CommentSerializer(
            comment_object, data=request_data, partial=True
        )
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        response_data = {"data": comment_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, comment_id=None, format=None):
        comment_object = self.get_object(comment_id=comment_id)

        self.check_object_permissions(request, comment_object)

        comment_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
