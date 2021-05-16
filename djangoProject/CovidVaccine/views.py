from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context

from .models import *
import math

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
        if not Userlogin.objects.filter(email=email).exists():
            return HttpResponse("Can not find your email address, please reenter or register")
        result = list(Userlogin.objects.filter(email=email).values('password'))[0]['password']
        if result == password:
            context = {"SSN": list(Userlogin.objects.filter(email=email).values('ssn'))[0]['ssn'],
                       "Email": email,
                       "Password": password}
            return render(request, 'userapi.html', context)
        else:
            return HttpResponse("Wrong password, try again")
    else:
        return HttpResponse("login failed you entered some null value")


def touserschedule(request):
    userssn = request.POST.get('SSN', '')
    context = {"SSN": userssn}
    ##return HttpResponse(request.POST.get('SSN', ''))
    return render(request, 'UserSchedule.html', context)


def inserttimeslot(SSN, weeklyslotid):
    for i in range(15):
        slotid_i = i * 14 + weeklyslotid
        new_slot_within_four_month = UserAvailability(ssn=SSN, slotid=slotid_i)
        new_slot_within_four_month.save()
    return


def verify_user_already_has_schedulue(SSN):
    if UserAvailability.objects.filter(ssn=SSN).exists():
        return 1
    return 0


def verify_user_already_has_travellimit(SSN):
    if UserTravelLimit.objects.filter(ssn=SSN).exists():
        return 1
    return 0

def verify_provider_already_has_travellimit(providerid):
    if ProviderTravelLimit.objects.filter(pid=providerid).exists():
        return 1
    return 0

def updateuserschedule(request):
    userssn = request.POST.get('SSN')
    userdistancelimit = request.POST.get('distancelimit', '')
    if not (userdistancelimit and userdistancelimit.isnumeric()):
        return HttpResponse("You must enter a valid distance!")
    if verify_user_already_has_travellimit(userssn):
        UserTravelLimit.objects.filter(ssn=userssn).delete()
    new_user_travel_limit = UserTravelLimit(ssn=userssn, distance=userdistancelimit)
    new_user_travel_limit.save()
    if verify_user_already_has_schedulue(userssn):
        UserAvailability.objects.filter(ssn=userssn).delete()
    for i in range(1, 15):
        if request.POST.get(str(i)) == "True":
            inserttimeslot(userssn, i)
    return HttpResponse("Yo")


def verify_provider_already_has_week_schedulue(providerid,weekcount):
    if ProviderWeekLock.objects.filter(pid=providerid,week=weekcount).exists():
        return 1
    return 0


def providertoaddschedule(request):
    providerid = request.POST.get('pid')
    providerdistancelimit = request.POST.get('distancelimit', '')
    weekcount = request.POST.get('weekcount','')
    capacity = request.POST.get('capacity')
    if not (providerdistancelimit and providerdistancelimit.isnumeric()):
        return HttpResponse("You must enter a valid distance!")
    if not (weekcount and weekcount.isnumeric()):
        return HttpResponse("You must enter a valid weekcount!")
    if not (capacity and capacity.isnumeric()):
        return HttpResponse("You must enter a valid capacity!")
    if (int(capacity) <= 0) :
        return HttpResponse("Capacity must be positive")
    if verify_provider_already_has_week_schedulue(providerid,weekcount):
        return HttpResponse("You have already added that week schedule")
    if verify_provider_already_has_travellimit(providerid):
        ProviderTravelLimit.objects.filter(pid=providerid).delete()
    new_provider_travel_limit = ProviderTravelLimit(pid=providerid, distance=providerdistancelimit)
    new_provider_travel_limit.save()
    new_week_appointment = ProviderWeekLock(pid=providerid,week=weekcount)
    new_week_appointment.save()
    for i in range(1, 15):
        if request.POST.get(str(i)) == "True":
            new_slot_id = 14 * (int(weekcount)-1) + i
            for j in range(int(capacity)):
                new_slot = ProviderAvailability(pid=providerid,slotid=new_slot_id)
                new_slot.save()
    return HttpResponse("Yo")


def touserregister(request):
    return render(request, 'userRegister.html')


def toproviderapi(request):
    providerid = request.POST.get("providerid", '')
    if not providerid:
        return HttpResponse("Enter a valid answer please")
    if not Provider.objects.filter(pid=providerid).exists():
        return HttpResponse("Enter a valid provider please")
    context = {"pid": providerid}
    return render(request, 'providerapi.html', context)


def toproviderregister(request):
    return render(request, 'providerRegister.html')


def toproviderschedule(request):
    pid = request.POST.get('pid', '')
    context = {'pid': pid}
    return render(request, 'ProviderSchedule.html', context)


def tohelp(request):
    listshit = list(Distance.objects.values("pid", "ssn", "distance"))
    for i in listshit:
        print(i['pid'], i['ssn'], i['distance'])
    return HttpResponse(listshit)


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
    if not (
            SSN.isnumeric() and Age.isnumeric() and Phone.isnumeric() and Zipcode.isnumeric() and LocationX.isnumeric() and LocationY.isnumeric()):
        return HttpResponse("you have entered non number thing which are supposed to be numbers")
    if User.objects.filter(ssn=SSN).exists():
        return HttpResponse("SSN already in our database")
    user = User(name=name, ssn=SSN, age=Age, phone=Phone, priorityid=prioritygroup)
    user.save()
    logininfo = Userlogin(email=Email, password=Password, ssn=SSN)
    logininfo.save()
    address = Useraddress(street=Street, city=city, state=State, zipcode=Zipcode, locationx=LocationX,
                          locationy=LocationY, ssn=SSN)
    address.save()
    f = lambda x1, y1, x2, y2: math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    listproviderinfo = list(Provideraddress.objects.values("pid", "locationx", "locationy"))
    for i in listproviderinfo:
        provider_i_pid = i['pid']
        provider_i_locationx = i['locationx']
        provider_i_locationy = i['locationy']
        distancebetweenmeandprovider_i = f(int(LocationX), int(LocationY), int(provider_i_locationx),
                                           int(provider_i_locationy))
        distance_me_i = Distance(ssn=SSN, pid=provider_i_pid, distance=distancebetweenmeandprovider_i)
        distance_me_i.save()
    return HttpResponse("Successfully Registered!")
