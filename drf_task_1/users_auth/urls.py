from django.urls import path
from .views import *

urlpatterns = [
    path('register/',UserRegister.as_view(),name="register"),
    path('userlist/',UserList.as_view(),name="userlist"),
    path('login/',Login.as_view(),name="login"),
    path('userbyid/<int:pk>',UserGetById.as_view(),name="userbyid"),
]