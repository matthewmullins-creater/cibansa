from django.conf.urls import url
from django.conf.urls import include
# from rest_framework import routers

from accounts import views
# from. import api


urlpatterns = [
    url(r'^sign-up',views.register,name="account-sign-up"),
    url(r'^login',views.login,name="account-login"),
    url(r'^logout',views.logout,name="account-logout"),
]