from django.urls import path
from kuning.views import *

app_name = 'kuning'

urlpatterns = [
    path('landing/', show_landing_page, name='landing'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('register/form/', register_form, name='register_form'),
    path('profile/', profile, name='profile'),
    path('profile/update/', profile_form, name='profile_form'),
    path('logout/', logout_user, name='logout'),
]