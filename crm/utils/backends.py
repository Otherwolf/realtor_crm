from django.conf import settings
from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):

    @staticmethod
    def _get_username_attempts_cache_key(username) -> str:
        cache_key = [
            'CustomModelBackend',
            'userLoginAttemptsCount',
            str(username)
        ]
        cache_key = ';'.join(cache_key)
        return cache_key

    @staticmethod
    def _get_user_id_login_attempts_cache():
        if settings.AUTHENTICATION_FAILED_ATTEMPTS_CACHE_KEY:
            from django.core.cache import caches
            cache = caches[settings.AUTHENTICATION_FAILED_ATTEMPTS_CACHE_KEY]
        else:
            from django.core.cache import cache
        return cache

    @staticmethod
    def is_user_failed_attempts_exceeded(username):
        cache = CustomModelBackend._get_user_id_login_attempts_cache()
        attempts = cache.get(CustomModelBackend._get_username_attempts_cache_key(username)) or 0
        return bool(attempts >= settings.AUTHENTICATION_FAILED_ATTEMPTS_LIMIT)

    def authenticate(self, request, username=None, password=None, **kwargs):
        from django.contrib.auth import get_user_model
        # noinspection PyPep8Naming
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            check_password = user.check_password(password)
            if not check_password:
                cache = self._get_user_id_login_attempts_cache()
                attempts = cache.get(self._get_username_attempts_cache_key(user.username)) or 0
                if attempts < settings.AUTHENTICATION_FAILED_ATTEMPTS_LIMIT:
                    attempts += 1
                    cache.set(
                        self._get_username_attempts_cache_key(user.username),
                        attempts,
                        settings.AUTHENTICATION_FAILED_ATTEMPTS_CACHE_STORE_TIMEOUT
                    )
            if check_password and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user) and not self.is_user_failed_attempts_exceeded(user.username)


__all__ = ('CustomModelBackend',)
