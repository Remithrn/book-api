from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import status
import requests


class ReauthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the request is forbidden or unauthorized, try refreshing the token
        if response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
        ]:
            print("Attempting token refresh...")

            # Get the refresh token from cookies
            refresh_token = request.COOKIES.get(
                settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]
            )

            if refresh_token:
                try:
                    # Attempt to refresh the token
                    refresh_url = f"{settings.SITE_URL}/api/auth/token/refresh/"
                    new_tokens = requests.post(
                        refresh_url, data={"refresh": refresh_token}
                    )

                    if new_tokens.status_code == 200:
                        new_access = new_tokens.json().get("access")

                        if new_access:
                            # Set the new access token in cookies
                            response.set_cookie(
                                key=settings.REST_AUTH["JWT_AUTH_COOKIE"],
                                value=new_access,
                                httponly=True,
                                samesite="Lax",
                            )

                            # Retry the original request
                            response = self.get_response(request)
                        else:
                            return JsonResponse(
                                {"detail": "Session expired. Please log in again."},
                                status=status.HTTP_401_UNAUTHORIZED,
                            )

                    else:
                        return JsonResponse(
                            {"detail": "Session expired. Please log in again."},
                            status=status.HTTP_401_UNAUTHORIZED,
                        )

                except (InvalidToken, TokenError):
                    return JsonResponse(
                        {"detail": "Invalid token."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

        return response
