from django.urls import path, include, re_path
# from rest_framework import routers

from accounts import views
# from. import api


urlpatterns = [
    path('sign-up',views.register,name="account-sign-up"),
    path('login',views.login,name="account-login"),
    path('logout',views.logout,name="account-logout"),
    path('forgot-password',views.ForgetPassword.as_view(),name="forgot-password"),
    path('reset-sent/', views.reset_sent, name="reset-sent"),
    path('profile/',views.profile,name="account-profile"),
    re_path(r'^reset/(?P<token>[\w:-]+)/$', views.PasswordReset.as_view(), name='password-reset'),
    path('reset-done/', views.reset_done, name="reset_done"),
]