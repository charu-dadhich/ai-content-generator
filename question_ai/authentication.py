from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import get_user_model
import time
from utils import (
    Helper,
    Responder
)

User = get_user_model()


class UserTokenAuthentication(BasicAuthentication):
    def authenticate(self, request):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return None
        payload = Helper.decode_jwt(access_token)
        if not (user := User.objects.get_by_pk(payload['id'])):
            Responder.throw_error(116)
        if not user.is_active:
            Responder.accept(117)
        current_epoch = int(time.time())
        if payload['exp'] <= current_epoch:
            Responder.throw_error(123)
        return (user, None)
