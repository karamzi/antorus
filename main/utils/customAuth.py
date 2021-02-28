from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend


class CustomAuth(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            print(user)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
