from django.shortcuts import render

# Create your views here.
def show_mypay(request):
    return render(request, 'mypay.html')

def show_transaksi(request):
    return render(request, 'transaksi.html')

def show_jasa(request):
    return render(request, 'jasa.html')

def show_status(request):
    return render(request, 'status.html')