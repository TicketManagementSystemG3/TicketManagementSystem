from django.urls import path
from account.api.views import SignupApiView
from account.api.views import UserCreationView
from account.api.views import ProfileView


app_name = 'account'

urlpatterns = [
    path("signup",SignupApiView.as_view(),name="signup"),
    path("create_user",UserCreationView().as_view(),name="create_user"),
    path("profile/<int:pk>",ProfileView.as_view(),name="profile")
]