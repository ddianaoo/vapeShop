from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('users/', ListUsers.as_view(), name='user_list'),
    path('add-assistant/', add_assistant, name='add_assistant'),
]
