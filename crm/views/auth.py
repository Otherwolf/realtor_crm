from uuid import uuid4

from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import (TemplateView, RedirectView)

from crm import forms
from project import settings

User = get_user_model()


class LoginView(TemplateView):
    template_name: str = 'auth/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            url = reverse('base', args=args, kwargs=kwargs)
            return HttpResponseRedirect(url)
        login_form = forms.LoginForm()
        if 'login_form' not in kwargs:
            kwargs.update(dict(login_form=login_form))
        return super().get(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_form = forms.LoginForm(request.POST)

        login_form.full_clean()
        if login_form.is_valid():
            username = User.normalize_username(login_form.cleaned_data['email'])
            user_exists = User.objects.filter(username=username).exists()

            if not user_exists:
                login_form.add_error('email', 'Пользователь не найден')

            user = authenticate(
                request,
                username=username,
                password=login_form.cleaned_data['password']
            )
            print(user)
            if user is None and user_exists:
                from crm.utils.backends import CustomModelBackend
                if CustomModelBackend.is_user_failed_attempts_exceeded(username):
                    login_form.add_error(
                        'email',
                        'Пользователь временно заблокирован за превышение количества '
                        'попыток входа. Пожалуйста, повторите попытку позже.'
                    )
                else:
                    login_form.add_error('password', 'Неверный пароль')

            if user:
                login(request, user)

                url = reverse('base', args=args, kwargs=kwargs)
                return HttpResponseRedirect(url)
            else:
                kwargs['login_form'] = login_form
                return self.get(request, *args, **kwargs)
        else:
            kwargs.update(dict(login_form=login_form))
            return self.get(request=request, *args, **kwargs)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class PasswordResetRequestView(TemplateView):
    template_name = 'auth/password_reset_request.html'

    def get(self, request, *args, **kwargs):
        return super().get(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        reset_form = forms.PasswordResetRequestForm(request.POST)
        email = reset_form['email'].value()
        if reset_form.is_valid():
            token = str(uuid4())
            email = reset_form.cleaned_data['email']
            user = User.objects.filter(email=email)
            if user:
                id = user[0].id
                key_cache = 'reset_user_password_' + token
                cache.set(key_cache, str(id), 60 * 60 * 24)
                url_password = request.get_host() + '/resetpas/' + token
                html_template = 'mail/user_reset_password_mail.html'
                msg_tmpl = get_template(html_template)
                message = msg_tmpl.render({'url': url_password})
                send_mail('Восстановление пароля', '', settings.EMAIL_HOST_USER, [email], html_message=message)
                url = reverse('password_reset_reset')
                return HttpResponseRedirect(url)
            else:
                reset_form.add_error('email', 'Пользователя с таким email не существует ')
        kwargs.update(dict(reset_form=reset_form))
        return super().get(request=request, *args, **kwargs)


__all__ = ('LoginView', 'LogoutView', 'PasswordResetRequestView',)
