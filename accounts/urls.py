from django.urls import path
from .views import (
    RegisterView,
    VerifyEmailView,
    LoginView,
    CustomPasswordResetView,
    CustomChangePasswordView,
    CustomPasswordResetConfirmView,
    ProfileViewList,
    FavoriteList,
    FavoriteDetail,
    UserProfileView,
    DeleteAccountView,
    MessageListView,
    search
)
urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("verify/email", VerifyEmailView.as_view(), name="verify email"),
    path("login", LoginView.as_view(), name="login"),
    path("password/reset", CustomPasswordResetView.as_view(), name="password reset"),
    path("password/reset/confirm", CustomPasswordResetConfirmView.as_view(), name="confirm password reset"),
    path("change/password", CustomChangePasswordView.as_view(), name="change password"),
    path("account/view/profile", UserProfileView.as_view(), name="profile_view"),
    path("account/view/profile/list", ProfileViewList.as_view(), name="profile view list"),
    path("favorite/list", FavoriteList.as_view(), name="favorite list"),
    path("favorite-detail/<int:pk>", FavoriteDetail.as_view(), name="favorite detail"),
    path('message/list', MessageListView.as_view(), name='message list'),
    path("account/delete", DeleteAccountView, name="delete account"),
    path("account/search", search, name="search"),
]
