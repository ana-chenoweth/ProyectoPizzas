from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(), name='login'),
    path("register/", views.register, name="register"), 
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),


    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name="password_reset_complete"),

    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]
