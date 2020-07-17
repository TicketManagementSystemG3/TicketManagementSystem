from django.urls import path,include
from account.api.views import ( 
                                SignupApiView,
                                UserCreationView,
                                ProfileView,
                                EnableDisableUserView,
                                PasswordChangeView,
                                 )
from rest_framework.authtoken.views import obtain_auth_token



app_name = 'account'

urlpatterns = [
    path("signup",SignupApiView.as_view(),name="signup"),
    path("create_user",UserCreationView().as_view(),name="create_user"),
    path("profile/<int:pk>",ProfileView.as_view(),name="profile"),
    path("disable_users/<slug:slug>",EnableDisableUserView.as_view()),
    path("disable_users/<slug:slug>/<int:pk>",EnableDisableUserView.as_view(),name="disable"),
    path("login",obtain_auth_token,name="login"),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("password_change",PasswordChangeView.as_view(),name="password_change")
]

