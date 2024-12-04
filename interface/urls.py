from django.urls import path


from interface.views import UserCreateView, SmsCodeView, UserDetailView, UserUpdateView
from interface.apps import InterfaceConfig

app_name = InterfaceConfig.name

urlpatterns = [
    path('', UserCreateView.as_view(), name='login'),
    path('sms_code', SmsCodeView.as_view(), name='sms_code'),
    path('user_detail', UserDetailView.as_view(), name='user_detail'),
    path('user_update', UserUpdateView.as_view(), name='user_update'),
]
