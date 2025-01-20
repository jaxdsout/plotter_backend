from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from ..seed import seed_test_account


class SandboxMiddleware(MiddlewareMixin):
    def process_request(self, request):
        SANDBOX_USERNAME = "aptatlas.test@gmail.com"

        if request.path == "/jwt/create/" and request.method == "POST":
            auth_header = request.META.get('HTTP_AUTHORIZATION', None)
            if auth_header:
                try:
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(auth_header.split()[1])

                    user = jwt_auth.get_user(validated_token)
                    if user.email == SANDBOX_USERNAME:
                        seed_test_account(user)

                except Exception as e:
                    print(f"Middleware error: {e}")
                    return None
            return None
