from django.forms import Form, fields


class LoginForm(Form):
    email = fields.CharField(required=True, label='Имя пользователя')
    password = fields.CharField(required=True, label='Пароль')


class PasswordResetRequestForm(Form):
    email = fields.CharField(required=True, label='E-mail')


__all__ = ('LoginForm', 'PasswordResetRequestForm',)
