from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return
        if user.check_password(password):
            return user
        return
