from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCommentOwner(BasePermission):
    """
    To ensure only the rightful owner of comment
    resource can make changes
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.commenter_id == request.user


class IsFeedbackOwner(BasePermission):
    """
    To ensure only the rightful owner of feedback
    resource can make changes
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.consumer_id == request.user


class IsItemOwner(BasePermission):
    """
    To ensure only the rightful owner of item
    resource can make changes
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.producer_id == request.user


class IsAProducer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user

        return user.user_type == "producer"


class IsFeedbackResponseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.responder_id == request.user


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == SAFE_METHODS:
            return True

        return obj.user_id == request.user
