from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from apps.consumer_protection.serializers.feedbacks_serializer import (
    FeedbacksSerializer,
    FeedbackResponseSerializer,
    FeedbackVerificationSerializer,
)
from apps.consumer_protection.models.feedbacks import (
    Feedbacks,
    FeedbackResponse,
    FeedbackVerifications,
)
from apps.consumer_protection.views.utils import CommonViewAttributes
from apps.consumer_protection.permissions.owner_permission import (
    IsFeedbackOwner,
    IsAProducer,
    IsFeedbackResponseOwner,
)


class FeedbackListCreateView(CommonViewAttributes, APIView):
    """
    View to process list and create requests
    for a feedback resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        feedback_objects = Feedbacks.objects.select_related(
            "consumer_id", "item_id"
        )
        feedback_serializer = FeedbacksSerializer(
            feedback_objects, many=True
        )

        response_data = {"data": feedback_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_feedback_data = Feedbacks.objects.create(**request_data)

        feedback_serializer = FeedbacksSerializer(
            data=new_feedback_data
        )
        feedback_serializer.is_valid(raise_exception=True)
        feedback_serializer.save(consumer_id=request.user)

        response_data = {"data": feedback_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class FeedbackRetrieveUpdateDestroyView(CommonViewAttributes, APIView):
    """
    View to handle retrieve, update, and delete
    request for a feedback resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsFeedbackOwner]

    def get_object(self, feedback_id):
        return Feedbacks.objects.select_related(
            "consumer_id", "item_id"
        ).get(feedback_id=feedback_id)

    def get(self, request, feedback_id=None, format=None):
        feedback_object = self.get_object(feedback_id=feedback_id)

        feedback_serializer = FeedbacksSerializer(feedback_object)

        response_data = {"data": feedback_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, feedback_id=None, format=None):
        feedback_object = self.get_object(feedback_id=feedback_id)
        request_data = request.data.get("body", feedback_object.body)

        self.check_object_permissions(request, feedback_object)

        feedback_serializer = FeedbacksSerializer(
            feedback_object, data=request_data, partial=True
        )
        feedback_serializer.is_valid(raise_exception=True)
        feedback_serializer.save()

        response_data = {"data": feedback_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, feedback_id=None, format=None):
        feedback_object = self.get_object(feedback_id=feedback_id)

        self.check_object_permissions(request, feedback_object)

        feedback_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedbackResponseListCreateView(CommonViewAttributes, APIView):
    """
    View to process list and create request
    for a feedback response resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsAProducer]

    def get(self, request, format=None):
        feedback_response_object = (
            FeedbackResponse.objects.select_related(
                "responder_id", "feedback_id"
            )
        )

        feedback_response_serializer = FeedbackResponseSerializer(
            feedback_response_object, many=True
        )

        response_data = {"data": feedback_response_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_feedback_response_object = FeedbackResponse.objects.create(
            **request_data
        )

        self.check_object_permissions(
            request, new_feedback_response_object
        )

        feedback_response_serializer = FeedbackResponseSerializer(
            data=new_feedback_response_object
        )
        feedback_response_serializer.is_valid(raise_exception=True)
        feedback_response_serializer.save(responder_id=request.user)

        response_data = {"data": feedback_response_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class FeedbackResponseRetrieveUpdateDestroyView(
    CommonViewAttributes, APIView
):
    """
    View to process retrieve, update, and delete request
    for a feedback response resource

    Requires an authentication token
    """

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAProducer,
        IsFeedbackResponseOwner,
    ]

    def get_object(self, feedback_response_id):
        return FeedbackResponse.objects.select_related(
            "feedback_id", "responder_id"
        ).get(feedback_response_id=feedback_response_id)

    def get(self, request, feedback_response_id=None, format=None):
        feedback_response_object = self.get_object(feedback_response_id)

        feedback_response_serializer = FeedbackResponseSerializer(
            feedback_response_object
        )

        response_data = {"data": feedback_response_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, feedback_response_id=None, format=None):
        feedback_response_object = self.get_object(feedback_response_id)

        self.check_object_permissions(request, feedback_response_object)

        data = request.data.get("body", feedback_response_object.body)

        feedback_response_serializer = FeedbackResponseSerializer(
            feedback_response_object, data=data
        )
        feedback_response_serializer.is_valid(raise_exception=True)
        feedback_response_serializer.save()

        response_data = {"data": feedback_response_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, feedback_response_id=None, format=None):
        feedback_response_object = self.get_object(feedback_response_id)

        self.check_object_permissions()

        feedback_response_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedbackVerificationListCreateView(CommonViewAttributes, APIView):
    """
    View to process list and create request for a
    feedback verifications resource

    Requires an authentication token
    """

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        feedback_verifications_object = (
            FeedbackVerifications.objects.select_related("feedback_id")
        )

        fback_verif_serialiazer = FeedbackVerificationSerializer(
            feedback_verifications_object, many=True
        )

        response_data = {"data": fback_verif_serialiazer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_feedback_verification_object = (
            FeedbackVerifications.objects.create(**request_data)
        )

        self.check_object_permissions(
            request, new_feedback_verification_object
        )

        fback_verif_serializer = FeedbackVerificationSerializer(
            data=new_feedback_verification_object
        )
        fback_verif_serializer.is_valid(raise_exception=True)
        fback_verif_serializer.save()

        response_data = {"data": fback_verif_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class FeedbackVerificationRetrieveUpdateDestroyView(
    CommonViewAttributes, APIView
):
    """
    View to handle retrieve, update, and delete request
    for a feedback verification resource

    Requires an authentication token
    """

    permission_classes = [IsAdminUser]

    def get_object(self, feedback_verification_id):
        return FeedbackVerifications.objects.select_related(
            "feedback_id"
        )

    def get(self, request, feedback_verification_id=None, format=None):
        fback_verif_object = self.get_object(feedback_verification_id)

        fback_verif_serializer = FeedbackVerificationSerializer(
            fback_verif_object
        )

        response_data = {"data": fback_verif_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(
        self, request, feedback_verification_id=None, format=None
    ):
        fback_verif_object = self.get_object(feedback_verification_id)

        self.check_object_permissions(request, fback_verif_object)

        request_data = request.data.get(
            "genuine", fback_verif_object.genuine
        )

        fback_verif_serializer = FeedbackVerificationSerializer(
            fback_verif_object, data=request_data
        )
        fback_verif_serializer.is_valid(raise_exception=True)
        fback_verif_serializer.save()

        response_data = {"data": fback_verif_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(
        self, request, feedback_verification_id=None, format=None
    ):
        fback_verif_object = self.get_object(feedback_verification_id)

        self.check_object_permissions(request, fback_verif_object)

        fback_verif_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
