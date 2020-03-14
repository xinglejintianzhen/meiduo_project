from django.urls import re_path

from . import views


urlpatterns = [

    re_path(r'^qq/login/$', views.QQAuthURLView.as_view()),
    re_path(r'^oauth_callback/$', views.QQAuthUserView.as_view()),
]