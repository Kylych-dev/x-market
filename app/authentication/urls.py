from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, VerifyEmail, LoginApiView, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordApiView, LogoutAPIView, AddToBlackListView, DeleteFromBlackListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'), 
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordApiView.as_view(), name='password-reset-complete'),

    path('add-to-blacklist/<int:user_id>', AddToBlackListView.as_view(), name='add-to-blacklist'),
    path('remove-from-blacklist/<int:user_id>', DeleteFromBlackListView.as_view(), name='remove-from-blacklist'),
]
