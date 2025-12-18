from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser

class PhoneNumberBackend(ModelBackend):
    """
    Authenticate using contact_number instead of username
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = CustomUser.objects.get(contact_number=username)
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
