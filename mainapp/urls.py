from django.urls import path
from .views import *

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/', home, name='home')
]