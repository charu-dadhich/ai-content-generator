from rest_framework.views import APIView
from question_ai.permissions import AllowAny
from utils import Responder
from .serializers import (
    LoginSerializer,
    ChangePasswordSerializer,
)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        data = user.login()
        return Responder.send(102, data)


class ChangePasswordView(APIView):

    def patch(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Responder.send(104)
