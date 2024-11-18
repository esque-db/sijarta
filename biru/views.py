from django.shortcuts import render, redirect
from django.contrib import messages

# --- TESTIMONI ---
def show_testimoni(request):
    # Dummy data untuk testimoni
    testimoni = [
        {'user': 'Alice', 'rating': 5, 'komentar': 'Sangat puas!', 'tanggal': '2024-11-01'},
        {'user': 'Bob', 'rating': 4, 'komentar': 'Layanan cukup baik.', 'tanggal': '2024-11-02'},
    ]
    return render(request, 'testimoni_list.html', {'testimoni': testimoni})

def add_testimoni(request):
    if request.method == 'POST':
        # Dummy form handling, nggak nyimpen ke mana-mana
        komentar = request.POST.get('komentar', '')
        rating = request.POST.get('rating', 5)
        messages.success(request, f"Testimoni berhasil ditambahkan! (Rating: {rating}, Komentar: {komentar})")
        return redirect('testimoni_list')
    return render(request, 'testimoni_form.html')

# --- VOUCHER ---
def show_vouchers(request):
    vouchers = [
        {'id': 1, 'kode': 'DISKON10', 'diskon': '10%', 'harga': 10000},
        {'id': 2, 'kode': 'POTONGAN50K', 'diskon': 'Rp50.000', 'harga': 60000},
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

    if user_balance >= voucher['harga']:
        return render(
            request,
            'voucher_list.html',
            {
                'vouchers': vouchers,
                'modal_sukses': True,
                'kode': voucher['kode'],
                'tanggal': voucher['tanggal'],
                'kuota': voucher['kuota'],
            },
        )
    else:
        return render(
            request,
            'voucher_list.html',
            {
                'vouchers': vouchers,
                'modal_gagal': True,
            },
        )
