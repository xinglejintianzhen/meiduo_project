from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count$', views.UsernameCountView.as_view()),
    re_path(r'^mobile/(?P<mobile>1[3-9]\d{9})/count$', views.UserMobileCountView.as_view()),
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户退出登录
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    re_path(r'^info/$', views.UserInfoView.as_view(), name='info'),
    re_path(r'^emails/$', views.EmailView.as_view(), name='email'),
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view(), name='email_verify'),
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view(), name='email_verify'),

]
