from rest_framework import serializers
from django.contrib.auth import get_user_model
from utils import (
    Responder,
    Validator,
)


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        if not (user := User.objects.get_by_email(attrs["email"])):
            Responder.accept(101)
        if user.check_password(attrs.get('password')):
            attrs["user"] = user
        else:
            Responder.accept(103)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)
    confirm_new_password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        instance = self.instance
        if not instance.check_password(attrs.get('old_password')):
            Responder.accept(112)
        Validator.validate_password(attrs.get('new_password'), attrs.get('old_password'))
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            Responder.accept(106)
        return attrs

    def update(self, instance, attrs):
        instance.set_password(attrs.get('new_password'))
        instance.save()
        return {}
