from django.conf.urls import url
from django.conf.urls import include
# from rest_framework import routers

from accounts import views
# from. import api


urlpatterns = [
    url(r'^sign-up',views.register,name="account-sign-up"),
    url(r'^login',views.login,name="account-login"),
    url(r'^logout',views.logout,name="account-logout"),
    url(r'^forgot-password',views.ForgetPassword.as_view(),name="forgot-password"),
    url(r'^reset-sent/', views.reset_sent, name="reset-sent"),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.PasswordReset.as_view(), name='password-reset'),
    url(r'^reset-done/', views.reset_done, name="reset_done"),
]