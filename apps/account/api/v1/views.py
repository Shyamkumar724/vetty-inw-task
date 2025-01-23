from rest_framework import generics
from rest_framework.views import Response
from apps.account.api.v1.serializers import LoginSerializer, SignUpSerializer
from rest_framework.validators import ValidationError
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView


@extend_schema(
    summary="Create a new user account",
    description=(
        "Account Create API which takes Email, Firstname, Lastname and Password.\n\n"
        "contains both uppercase and lowercase letters, and includes at least one \n"
        "special character."
    ),
    tags=["Account Module APIS"],
)
class SignUpView(generics.CreateAPIView):

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        self.response_format = dict()
        super().__init__(**kwargs)

    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            self.response_format["status"] = True
            self.response_format["status_code"] = status.HTTP_201_CREATED
            self.response_format["data"] = response.data
            self.response_format["message"] = "User Creation Successfull"
        except ValidationError as e:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["data"] = "None"
            self.response_format["message"] = {
                key: value for key, value in e.detail.items()
            }
            return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.response_format, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="User login",
    description="""
    This endpoint allows users to log in by providing their email and password.
    On successful authentication, it returns an access and refresh token,
    along with the user's email and username. \n\n
    the user's email and username.
    **Access Control:**
    - No authentication is required to access this endpoint.
    """,
    tags=["Account Module APIS"],
)
class LoginView(generics.GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def __init__(self, **kwargs):
        self.response_format = dict()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    self.response_format["success"] = True
                    self.response_format["status_code"] = status.HTTP_200_OK
                    self.response_format["data"] = {"token": token.key}
                    self.response_format["message"] = "User Login Successfull"
                    return Response(self.response_format, status=status.HTTP_200_OK)
                else:
                    self.response_format["success"] = False
                    self.response_format["status_code"] = status.HTTP_401_UNAUTHORIZED
                    self.response_format["data"] = "None"
                    self.response_format["message"] = "No User Found"
                    return Response(
                        {"error": "Invalid credentials"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except Exception as e:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_401_UNAUTHORIZED
            self.response_format["data"] = "None"
            self.response_format["message"] = str(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="User Logout",
    description="""
    This endpoint allows users to logout.
    **Access Control:**
    - authentication is required to access this endpoint.
    """,
    tags=["Account Module APIS"],
)
class LogoutView(APIView):
    """
    Handles user logout by deleting the authentication token.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.response_format = dict()
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            self.response_format["success"] = True
            self.response_format["status_code"] = status.HTTP_200_OK
            self.response_format["message"] = "User logged out successfully."
            self.response_format["data"] = "None"
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format["success"] = False
            self.response_format["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format["message"] = "Logout failed."
            self.response_format["data"] = str(e)
            return Response(
                self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
