from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

# --- TESTIMONI ---
def show_testimoni(request):
    # Dummy data untuk testimoni, bisa dihubungkan ke database kalau ada
    testimoni = [
        {'user': 'Alice', 'rating': 5, 'komentar': 'Sangat puas!', 'tanggal': '2024-11-01'},
        {'user': 'Bob', 'rating': 4, 'komentar': 'Layanan cukup baik.', 'tanggal': '2024-11-02'},
    ]
    return render(request, 'testimoni_list.html', {'testimoni': testimoni})

def add_testimoni(request):
    # Validasi apakah pengguna memiliki transaksi selesai (dummy validasi)
    has_finished_transaction = True  # Ubah sesuai logika database nanti
    if not has_finished_transaction:
        messages.error(request, "Anda tidak dapat memberikan testimoni sebelum menyelesaikan transaksi.")
        return redirect('testimoni_list')

    if request.method == 'POST':
        komentar = request.POST.get('komentar', '')
        rating = request.POST.get('rating', 5)

        if not (1 <= int(rating) <= 10):  # Validasi input rating
            messages.error(request, "Rating harus antara 1 sampai 10.")
            return redirect('add_testimoni')

        # Simpan testimoni ke database di sini kalau sudah ada model
        messages.success(request, f"Testimoni berhasil ditambahkan! (Rating: {rating}, Komentar: {komentar})")
        return redirect('testimoni_list')

    return render(request, 'testimoni_form.html')

# --- VOUCHER ---
def show_vouchers(request):
    # Dummy data untuk voucher dan promo
    vouchers = [
        {'id': 1, 'kode': 'DISKON10', 'diskon': '10%', 'harga': 10000, 'kuota': 3, 'tanggal': '2024-12-31'},
        {'id': 2, 'kode': 'POTONGAN50K', 'diskon': 'Rp50.000', 'harga': 60000, 'kuota': 1, 'tanggal': '2024-11-30'},
    ]
    promos = [
        {'kode': 'PROMO1', 'tanggal_akhir': '2024-12-31'},
        {'kode': 'PROMO2', 'tanggal_akhir': '2025-01-15'},
    ]
    return render(request, 'voucher_list.html', {'vouchers': vouchers, 'promos': promos})

def beli_voucher(request, voucher_id):
    user_balance = 50000  # Dummy saldo pengguna
    vouchers = [
        {'id': 1, 'kode': 'DISKON10', 'harga': 10000, 'tanggal': '2024-12-31', 'kuota': 3},
        {'id': 2, 'kode': 'POTONGAN50K', 'harga': 60000, 'tanggal': '2024-11-30', 'kuota': 1},
    ]

    voucher = next((v for v in vouchers if v['id'] == voucher_id), None)
    if not voucher:
        messages.error(request, "Voucher tidak ditemukan.")
        return redirect('voucher_list')

    # Validasi saldo pengguna
    if user_balance < voucher['harga']:
        messages.error(request, "Saldo Anda tidak mencukupi untuk membeli voucher ini.")
        return redirect('voucher_list')

    # Validasi kuota penggunaan dan masa berlaku
    if voucher['kuota'] <= 0:
        messages.error(request, "Kuota voucher sudah habis.")
        return redirect('voucher_list')

    if datetime.strptime(voucher['tanggal'], '%Y-%m-%d') < datetime.now():
        messages.error(request, "Voucher sudah tidak berlaku.")
        return redirect('voucher_list')

    # Simpan pembelian voucher ke database di sini kalau sudah ada model
    messages.success(
        request,
        f"Selamat! Anda berhasil membeli voucher {voucher['kode']} yang berlaku hingga {voucher['tanggal']}."
    )
    return redirect('voucher_list')
