from django.urls import path
from hijau.views import *

app_name = 'hijau'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('pekerja/', homepage_pekerja, name='homepage_pekerja'),
    path('subkategori/<str:kategori>/<str:subkategori>/', subkategori, name='subkategori'),
    path('subkategori/<str:kategori>/<str:subkategori>/pekerja', subkategoripekerja, name='subkategoripekerja'),
    path('pekerja/<int:pekerja_id>/', profil_pekerja, name='profil_pekerja'),
    path('pesan-jasa/', pesan_jasa, name='pesan_jasa'),
    path('view-pemesanan-jasa/', view_pemesanan_jasa, name='view_pemesanan_jasa'),
    path('subkategori/<str:kategori>/<str:subkategori>/bergabung/', bergabung_subkategori, name='bergabung_subkategori'),

]