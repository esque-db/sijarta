from django.urls import path
from merah.views import show_mypay, show_jasa, show_status, show_transaksi

app_name = 'merah'

urlpatterns = [
    path("mypay/", show_mypay, name="show_mypay"),
    path("mypay/transaksi", show_transaksi, name="show_transaksi"),
    path("jasa/", show_jasa, name="show_jasa"),
    path("status/", show_status, name="show_status"),
]