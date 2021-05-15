from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
from django.template.defaulttags import csrf_token


def tocovidvaccine(request):
    return render(request, 'covidvaccinemain.html')


def touserlogin(request):
    return render(request, 'userlogin.html')


def toproviderlogin(request):
    return render(request, 'providerlogin.html')


def touserapi(request):
    email = request.POST.get("Email", '')
    password = request.POST.get("Password", '')
    if email and password:
        return HttpResponse("successful login")
    else:
        return HttpResponse("login failed")
    return render(request, 'userapi.html')


def touserregister(request):
    return render(request, 'userRegister.html')


def toproviderapi(request):
    return render(request, 'providerapi.html')


def toproviderregister(request):
    return render(request, 'providerRegister.html')


def touserregisterdatainput(request):
    name = request.POST.get("name", '')
    SSN = request.POST.get("SSN", '')
    if len(SSN) != 9:
        return HttpResponse("Wrong SSN NUMBER!")
    Age = request.POST.get("Age", '')
    Phone = request.POST.get("Phone", '')
    if len(Phone) != 10:
        return HttpResponse("Wrong Phone NUMBER!")
    if not (Age.isnumeric()):
        return HttpResponse("Age should be number!")
    intage = int(Age)
    prioritygroup = 4
    if intage >= 70:
        prioritygroup = 1
    elif intage >= 55:
        prioritygroup = 2
    elif intage >= 40:
        prioritygroup = 3
    Email = request.POST.get("Email", '')
    Password = request.POST.get("Password", '')
    Street = request.POST.get("Street", '')
    city = request.POST.get("city", '')
    State = request.POST.get("State", '')
    Zipcode = request.POST.get("Zipcode", '')
    if len(Zipcode) != 5:
        return HttpResponse("Wrong zipcode Number")
    LocationX = request.POST.get("LocationX", '')
    LocationY = request.POST.get("LocationY", '')
    if not (
            name and SSN and Age and Phone and Email and Password and Street and city and State and Zipcode and LocationX and LocationY):
        return HttpResponse("you have failed")
    if not (SSN.isnumeric() and Age.isnumeric() and Phone.isnumeric() and Zipcode.isnumeric() and LocationX.isnumeric() and LocationY.isnumeric()):
        return HttpResponse("you have entered non number thing which are supposed to be numbers")
    user = User(name=name,ssn=SSN,age =Age, phone = Phone,prioirtyid=prioritygroup)
    user.save()
    logininfo = Userlogin(email=Email, password=Password)
    logininfo.save()
    address = Useraddress(street=Street, city=city, state=State, zipcode=Zipcode, locationx=LocationX,
                                      locationy=LocationY)
    address.save()

    return
