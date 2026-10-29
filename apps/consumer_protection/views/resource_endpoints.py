from rest_framework.reverse import reverse


def get_resource_endpoints(request, format):
    return [
        {
            "comment-list": reverse(
                "comment-list", request=request, format=format
            )
        },
        {
            "comment-detail": reverse(
                "comment-detail",
                request=request,
                format=format,
                kwargs={"comment_id": "resource_UUID"},
            )
        },
        {
            "feedback-list": reverse(
                "feedback-list", request=request, format=format
            )
        },
        {
            "feedback-detail": reverse(
                "feedback-detail",
                request=request,
                format=format,
                kwargs={"feedback_id": "resource_UUID"},
            )
        },
        {
            "feedback-response-list": reverse(
                "feedback-response-list", request=request, format=format
            )
        },
        {
            "feedback-response-detail": reverse(
                "feedback-response-detail",
                request=request,
                format=format,
                kwargs={"feedback_response_id": "resource_UUID"},
            )
        },
        {
            "feedback-verification-list": reverse(
                "feedback-verification-list",
                request=request,
                format=format,
            )
        },
        {
            "feedback-verification-detail": reverse(
                "feedback-verification-detail",
                request=request,
                format=format,
                kwargs={"feedback_verification_id": "resource_UUID"},
            )
        },
        {
            "item-list": reverse(
                "item-list", request=request, format=format
            )
        },
        {
            "item-detail": reverse(
                "item-detail",
                request=request,
                format=format,
                kwargs={"item_id": "resource_UUID"},
            )
        },
        {
            "leaderboard-list": reverse(
                "leaderboard-list", request=request, format=format
            )
        },
        {
            "leaderboard-detail": reverse(
                "leaderboard-detail",
                request=request,
                format=format,
                kwargs={"leaderboard_id": "resource_UUID"},
            )
        },
        {
            "user-list": reverse(
                "user-list", request=request, format=format
            )
        },
        {
            "user-detail": reverse(
                "user-detail",
                request=request,
                format=format,
                kwargs={"user_id": "resource_UUID"},
            ),
        },
        {"sign-in": reverse("sign-in", request=request, format=format)},
        {
            "sign-out": reverse(
                "sign-out", request=request, format=format
            )
        },
        {
            "register": reverse(
                "register", request=request, format=format
            )
        },
    ]
