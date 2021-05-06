from django.shortcuts import render

# Create your views here.

def tocovidvaccine(request):
    return render(request,'covidvaccinemain.html')

def touserlogin(request):
    return render(request,'userlogin.html')

def toproviderlogin(request):
    return render(request,'providerlogin.html')

def touserapi(request):
    return render(request,'userapi.html')

def touserregister(request):
    return render(request,'userRegister.html')

def toproviderapi(request):
    return render(request,'providerapi.html')

def toproviderregister(request):
    return render(request,'providerRegister.html')
