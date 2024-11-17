from django.shortcuts import render, redirect
from django.contrib import messages

def homepage(request):
    # Hardcode data for categories and subcategories
    data = {
        'Kategori Jasa 1': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
        'Kategori Jasa 2': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
        'Kategori Jasa 3': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
    }

    # Filter data based on query parameters
    kategori_filter = request.GET.get('kategori')
    subkategori_filter = request.GET.get('subkategori')

    if kategori_filter:
        data = {k: v for k, v in data.items() if k == kategori_filter}

    if subkategori_filter:
        data = {k: [sub for sub in v if subkategori_filter.lower() in sub.lower()] for k, v in data.items()}

    # Pass the category names for the dropdown
    kategori_list = list(data.keys())

    context = {
        'data': data,
        'kategori_list': ['Kategori Jasa 1', 'Kategori Jasa 2', 'Kategori Jasa 3']
    }
    return render(request, 'homepage.html', context)

def homepage_pekerja(request):
    # Hardcode data for categories and subcategories
    data = {
        'Kategori Jasa 1': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
        'Kategori Jasa 2': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
        'Kategori Jasa 3': ['Subkategori Jasa 1', 'Subkategori Jasa 2', 'Subkategori Jasa 3'],
    }

    # Filter data based on query parameters
    kategori_filter = request.GET.get('kategori')
    subkategori_filter = request.GET.get('subkategori')

    if kategori_filter:
        data = {k: v for k, v in data.items() if k == kategori_filter}

    if subkategori_filter:
        data = {k: [sub for sub in v if subkategori_filter.lower() in sub.lower()] for k, v in data.items()}

    # Pass the category names for the dropdown
    kategori_list = list(data.keys())

    context = {
        'data': data,
        'kategori_list': ['Kategori Jasa 1', 'Kategori Jasa 2', 'Kategori Jasa 3']
    }
    return render(request, 'homepage_pekerja.html', context)

DATA = {
    'Kategori Jasa 1': {
        'Subkategori Jasa 1': {
            'deskripsi': 'Deskripsi untuk Subkategori Jasa 1 di Kategori Jasa 1.',
            'sesi_layanan': [
                {'nama': 'Layanan A', 'harga': 50000},
                {'nama': 'Layanan B', 'harga': 75000},
            ],
            'pekerja': [
                {'nama': 'Pekerja 1', 'rating': 4.5, 'id': 1},
                {'nama': 'Pekerja 2', 'rating': 4.2, 'id': 2},
            ],
            'testimoni': [
                {'pengguna': 'User A', 'tanggal': '2024-11-17', 'pekerja': 'Pekerja 1', 'rating': 4.5, 'teks': 'Sangat puas!'},
                {'pengguna': 'User B', 'tanggal': '2024-11-16', 'pekerja': 'Pekerja 2', 'rating': 4.0, 'teks': 'Pelayanan baik.'},
            ],
        },
    },
}

PEKERJA_LIST = [
    {
        'id': 1,
        'nama': 'Andi Wirawan',
        'kategori': 'Kategori Jasa 1',
        'subkategori': 'Subkategori Jasa 1',
        'deskripsi': 'Berpengalaman selama 5 tahun dalam instalasi listrik rumah tangga.',
        'testimoni': [
            {'pengguna': 'Budi', 'isi': 'Layanan sangat memuaskan!'},
            {'pengguna': 'Ani', 'isi': 'Hasil pekerjaan rapi dan cepat.'},
        ],
        'layanan': [
            {'nama': 'Pasang Listrik 1 Fasa', 'harga': 'Rp 500.000'},
            {'nama': 'Pasang Listrik 3 Fasa', 'harga': 'Rp 1.000.000'},
        ],
        'rating': 9.5,
        'pesanan_selesai': 125,
        'no_hp': '08123456789',
        'tanggal_lahir': '12/01/1990',
        'alamat': 'Jl. Merdeka No. 45, Yogyakarta',
    },
    {
        'id': 2,
        'nama': 'Siti Rahmawati',
        'kategori': 'Kategori Jasa 1',
        'subkategori': 'Subkategori Jasa 1',
        'deskripsi': 'Mengatasi berbagai masalah AC dengan hasil memuaskan.',
        'testimoni': [
            {'pengguna': 'Dewi', 'isi': 'Teknisi yang sangat ramah dan profesional.'},
        ],
        'layanan': [
            {'nama': 'Service AC Standard', 'harga': 'Rp 150.000'},
            {'nama': 'Isi Ulang Freon', 'harga': 'Rp 200.000'},
        ],
        'rating': 9.5,
        'pesanan_selesai': 125,
        'no_hp': '08123456789',
        'tanggal_lahir': '12/01/1990',
        'alamat': 'Jl. Merdeka No. 45, Yogyakarta',
    },
]

# Fungsi untuk memeriksa apakah pengguna adalah pekerja
def is_worker(user):
    return getattr(user, 'is_worker', False)

def subkategori(request, kategori, subkategori):
    # Validasi kategori dan subkategori
    if kategori not in DATA or subkategori not in DATA[kategori]:
        return redirect('hijau:homepage')
    
    subkategori_data = DATA[kategori][subkategori]

    pekerja_list = [p for p in PEKERJA_LIST if p['kategori'] == kategori and p['subkategori'] == subkategori]
    context = {
        'kategori': kategori,
        'subkategori': subkategori,
        'deskripsi': subkategori_data.get('deskripsi'),
        'sesi_layanan': subkategori_data.get('sesi_layanan', []),
        'pekerja_list': pekerja_list,
        'testimoni': subkategori_data.get('testimoni', []),
        'is_worker': is_worker(request.user),  # Cek apakah pengguna adalah pekerja
    }

    # Logika tambahan untuk pekerja
    if context['is_worker']:
        # Tambahkan logika untuk pekerja jika diperlukan
        context['joined'] = any(worker['id'] == request.user.id for worker in subkategori_data['pekerja'])
    
    return render(request, 'subkategori.html', context)

def subkategoripekerja(request, kategori, subkategori):
    # Validasi kategori dan subkategori
    if kategori not in DATA or subkategori not in DATA[kategori]:
        return redirect('hijau:homepage')
    
    subkategori_data = DATA[kategori][subkategori]
    pekerja_list = [p for p in PEKERJA_LIST if p['kategori'] == kategori and p['subkategori'] == subkategori]
    context = {
        'kategori': kategori,
        'subkategori': subkategori,
        'deskripsi': subkategori_data.get('deskripsi'),
        'sesi_layanan': subkategori_data.get('sesi_layanan', []),
        'pekerja_list': pekerja_list,
        'testimoni': subkategori_data.get('testimoni', []),
        'is_worker': True,  # Cek apakah pengguna adalah pekerja
    }

    # Logika tambahan untuk pekerja
    if context['is_worker']:
        # Tambahkan logika untuk pekerja jika diperlukan
        context['joined'] = any(worker['id'] == request.user.id for worker in subkategori_data['pekerja'])
    
    return render(request, 'subkategori.html', context)


def profil_pekerja(request, pekerja_id):
    """
    View untuk menampilkan profil pekerja berdasarkan ID.
    Jika pekerja tidak ditemukan, akan diarahkan ke homepage.
    """
    # Cari pekerja berdasarkan ID
    pekerja = next((p for p in PEKERJA_LIST if p['id'] == pekerja_id), None)
    
    # Jika pekerja tidak ditemukan, arahkan ke halaman homepage
    if not pekerja:
        return redirect('hijau:homepage')  # Ganti 'hijau:homepage' dengan nama URL yang sesuai
    
    # Siapkan context untuk template
    context = {
        'pekerja': pekerja,
    }
    
    # Render halaman profil pekerja
    return render(request, 'profil_pekerja.html', context)

def pesan_jasa(request):
    if request.method == 'POST':
        tanggal_pemesanan = request.POST.get('tanggal_pemesanan')
        kode_diskon = request.POST.get('kode_diskon', '')
        total_pembayaran = 100000  # Contoh angka default (bisa diambil dari database)

        # Hitung diskon (jika ada kode diskon)
        if kode_diskon == "DISKON10":  # Contoh kode diskon
            total_pembayaran -= total_pembayaran * 0.1

        metode_pembayaran = request.POST.get('metode_pembayaran')

        # Simpan ke database atau proses lainnya
        # ... (Tambahkan logika penyimpanan di sini)

        # Pesan sukses dan redirect ke halaman View Pemesanan Jasa
        messages.success(request, 'Pesanan jasa berhasil dibuat!')
        return redirect('hijau:view_pemesanan_jasa')

    return render(request, 'pesan_jasa.html')

def view_pemesanan_jasa(request):
    # Contoh data dummy untuk pemesanan
    subkategori_list = ['Cleaning Service', 'Laundry', 'Tukang Kebun']
    daftar_pesanan = [
        {
            'id': 1,
            'subkategori': 'Cleaning Service',
            'sesi_layanan': 'Paket Harian',
            'harga': 100000,
            'nama_pekerja': 'John Doe',
            'status': 'Menunggu Pembayaran',
            'testimoni_dibuat': False,
        },
        {
            'id': 2,
            'subkategori': 'Laundry',
            'sesi_layanan': 'Paket Mingguan',
            'harga': 150000,
            'nama_pekerja': 'Jane Smith',
            'status': 'Pesanan Selesai',
            'testimoni_dibuat': False,
        },
        {
            'id': 3,
            'subkategori': 'Tukang Kebun',
            'sesi_layanan': 'Paket Bulanan',
            'harga': 200000,
            'nama_pekerja': None,
            'status': 'Mencari Pekerja Terdekat',
            'testimoni_dibuat': False,
        },
    ]

    subkategori_filter = request.GET.get('subkategori', '')
    status_filter = request.GET.get('status', '')

    # Terapkan filter jika ada
    if subkategori_filter:
        daftar_pesanan = [pesanan for pesanan in daftar_pesanan if pesanan['subkategori'] == subkategori_filter]
    if status_filter:
        daftar_pesanan = [pesanan for pesanan in daftar_pesanan if pesanan['status'] == status_filter]

    context = {
        'daftar_pesanan': daftar_pesanan,
        'subkategori_list': subkategori_list,
    }
    return render(request, 'view_pemesanan_jasa.html', context)