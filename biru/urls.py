from django.urls import path
from .views import show_testimoni, add_testimoni, show_vouchers, beli_voucher

app_name = 'biru'

urlpatterns = [
    # Testimoni
    path('testimoni/', show_testimoni, name='testimoni_list'),
    path('testimoni/add/', add_testimoni, name='testimoni_add'),

    # Voucher
    path('vouchers/', show_vouchers, name='voucher_list'),
    path('vouchers/buy/<int:voucher_id>/', beli_voucher, name='voucher_buy'),
]
