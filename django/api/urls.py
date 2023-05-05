from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('user/getUserDetails', UserView.as_view()),
    path('game/getGameProgress', GameProgressView.as_view()),
    path('game/setGameProgress', GameProgressUpdateView.as_view())
]
