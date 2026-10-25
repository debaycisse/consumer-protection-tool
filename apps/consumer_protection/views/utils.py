from rest_framework.authentication import TokenAuthentication


class CommonViewAttributes:
    """
    To collect and share common attributes among the view classes
    """

    authentication_classes = [TokenAuthentication]
