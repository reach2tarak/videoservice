from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('course/<slug>/', view_course, name="course"),
    path('become_pro/', become_pro, name="become_pro"),
    path('charge/', charge, name="charge"),
    path('login/', login_attempt, name="login_attempt"),
    path('register/', register_attempt, name="register_attempt"),
    path('logout/', logout_attempt, name="logout_attempt"),
]