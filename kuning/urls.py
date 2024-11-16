from django.urls import path
from kuning.views import *

app_name = 'kuning'

urlpatterns = [
    path('landing/', show_landing_page, name='landing'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/pelanggan/', register_pekerja, name='register_pekerja'),
]