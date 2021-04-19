from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from crm.views import auth
from crm.views import base, rest
from project import settings


def l(class_view):
    return login_required(class_view.as_view(), redirect_field_name='login')

urlpatterns = [
    path('logout', l(auth.LogoutView), name='logout'),
    path('login', auth.LoginView.as_view(), name='login'),
    path('password_reset/request', auth.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('rest/profile', l(rest.ProfileRest), name='rest_profile'),
    path('rest/load-data', l(rest.LoadDataRest), name='load_data_rest'),
    path('rest/load-main', l(rest.LoadMainRest), name='load_main_rest'),
    path('', l(base.BaseView), name='base')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
