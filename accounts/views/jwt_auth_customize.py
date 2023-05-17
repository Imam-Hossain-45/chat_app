from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import (
    jwt_response_payload_handler, JSONWebTokenAPIView, ObtainJSONWebToken, VerifyJSONWebToken, RefreshJSONWebToken
)
from accounts.serializers import UserSerializer


class CustomJSONWebTokenAPIView(JSONWebTokenAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Purpose: override jwt post function to achieve desired result
    """

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data['user'] = UserSerializer(user).data
            formatted_response = Response(response_data, status=status.HTTP_200_OK)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                formatted_response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True
                )

            return formatted_response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainJSONWebToken(ObtainJSONWebToken, CustomJSONWebTokenAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Workflow:
        1. API View that receives a POST with a user's username and password.
        2. Returns a JSON Web Token that can be used for authenticated requests.
    """


class CustomVerifyJSONWebToken(VerifyJSONWebToken, CustomJSONWebTokenAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Workflow:
        1. API View that checks the veracity of a token, returning the token if it is valid.
    """


class CustomRefreshJSONWebToken(RefreshJSONWebToken, CustomJSONWebTokenAPIView):
    """
    Author: A.G.M. Imam Hossain
    Date: May 12, 2023,
    Workflow:
        1. API View that returns a refreshed token (with new expiration) based on existing token
        2. If 'orig_iat' field (original issued-at-time) is found, will first check
            if it's within expiration window, then copy it to the new token
    """


obtain_jwt_token = CustomObtainJSONWebToken.as_view()
refresh_jwt_token = CustomRefreshJSONWebToken.as_view()
verify_jwt_token = CustomVerifyJSONWebToken.as_view()
