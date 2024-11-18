from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def show_landing_page(request):
    return render(request, 'landing.html')

def login_user(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        # You'll need to modify authenticate to use phone instead of username
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            user.is_pekerja = user.is_staff  # temporary solution
            user.is_pengguna = not user.is_staff
            return redirect('kuning:landing')  # redirect to homepage after login
        else:
            messages.error(request, 'No HP atau password salah.')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('kuning:login')

def register(request):
    return render(request, 'register.html')

def register_form(request):
    if request.method == "POST":
        role = request.POST.get('role', 'pengguna')
        # Add validation for required fields
        if not all(request.POST.get(field) for field in ['phone', 'password1', 'password2', 'nama']):
            messages.error(request, 'Semua field harus diisi.')
            return render(request, 'register_form.html', {'role': role})
            
        # Check if phone number is unique
        if User.objects.filter(phone=request.POST.get('phone')).exists():
            messages.error(request, 'No HP telah terdaftar.')
            return redirect('kuning:login')
            
        # For Pekerja, check NPWP and bank account uniqueness
        if role == 'pekerja':
            if User.objects.filter(npwp=request.POST.get('npwp')).exists():
                messages.error(request, 'NPWP telah terdaftar.')
                return render(request, 'register_form.html', {'role': role})
                
            if User.objects.filter(
                nama_bank=request.POST.get('nama_bank'),
                no_rekening=request.POST.get('no_rekening')
            ).exists():
                messages.error(request, 'Kombinasi nama bank dan no rekening telah terdaftar.')
                return render(request, 'register_form.html', {'role': role})
        
        # If all validations pass, create user
        # You'll need to implement the actual user creation logic here
        
        messages.success(request, 'Registrasi berhasil!')
        return redirect('kuning:login')
        
    return render(request, 'register_form.html', {'role': request.GET.get('role', 'pengguna')})

# @login_required
def profile(request):
    # Add these flags to determine user type
    # request.user.is_pekerja = request.user.is_staff
    # request.user.is_pengguna = not request.user.is_staff
    user = {
        "is_pekerja": False,
        "username": "FrankyRayMS",
        "level": 1,
        "gender": "Laki-Laki",
        "phone": "081234567890",
        "birth_date": "10-10-2010",
        "address": "Bogor",
        "balance": "Rp 123.456,78"
    }
    return render(request, 'profile.html', {'user': user})

def profile_form(request):
    if not request.user.is_authenticated:
        return redirect('kuning:login')
        
    if request.method == "POST":
        # Prevent updating restricted fields
        if request.user.is_pengguna:
            restricted_fields = ['balance', 'level']
        else:  # is_pekerja
            restricted_fields = ['balance', 'rating', 'jumlah_pesanan_selesai', 'kategori_pekerjaan']
            
        # Update only allowed fields
        # You'll need to implement the actual update logic here
        
        messages.success(request, 'Profile berhasil diupdate!')
        return redirect('kuning:profile')
        
    return render(request, 'profile_form.html')