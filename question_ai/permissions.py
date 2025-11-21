from rest_framework.permissions import BasePermission
from utils import Responder, helper


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True
    

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)