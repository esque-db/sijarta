from django.urls import path
from kuning.views import login_user

app_name = 'kuning'

urlpatterns = [
    path('login/', login_user, name='login')
]