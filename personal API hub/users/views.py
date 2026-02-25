from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

from rest_framework import status
from core.utils.responses import success_response, error_response

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data={"username": user.username, "email": user.email},
                message="User registered successfully.",
                status_code=status.HTTP_201_CREATED
            )
        return error_response("Registration failed.", status.HTTP_400_BAD_REQUEST, serializer.errors)
