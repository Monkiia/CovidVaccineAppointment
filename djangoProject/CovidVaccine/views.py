from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context

from .models import *
import math
import sqlite3

# Create your views here.
from django.template.defaulttags import csrf_token

def determinebaduser(ssn):
    if len(list(Baduser.objects.filter(ssn=ssn).values('ssn'))) >= 3:
        return 1
    return 0


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
            ssn = list(Userlogin.objects.filter(email=email).values('ssn'))[0]['ssn']
            if determinebaduser(ssn):
                return HttpResponse("You are a bad user. Go away!")
            context = {"SSN": ssn,
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
    if Appointment.objects.filter(ssn=userssn,user_accepted="pending"):
        return HttpResponse("You having pending appointment to check. You cannot modify schedule unless you decline your current appointment")
    if Appointment.objects.filter(ssn=userssn,user_accepted="True"):
        if Appointment.objects.filter(ssn=userssn,user_accepted="True",user_canceled="pending"):
            return HttpResponse("You already accepted an offer! No need to modify your schedule")
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
    provider_capacity = request.POST.get('capacity')
    if not (providerdistancelimit and providerdistancelimit.isnumeric()):
        return HttpResponse("You must enter a valid distance!")
    if not (weekcount and weekcount.isnumeric()):
        return HttpResponse("You must enter a valid weekcount!")
    if not (provider_capacity and provider_capacity.isnumeric()):
        return HttpResponse("You must enter a valid capacity!")
    if (int(provider_capacity) <= 0) :
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
            new_slot = ProviderAvailability(pid=providerid,slotid=new_slot_id,capacity=provider_capacity)
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
    # listshit = list(Distance.objects.values("pid", "ssn", "distance"))
    # for i in listshit:
    #     print(i['pid'], i['ssn'], i['distance'])
    ssn = 347000000
    return HttpResponse(determinebaduser(ssn))


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


def calculate_and_update(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    #查找 真实appointment table， 如果有user decline或者cancel了他的appointment
    #则将provider_availbility.capacity+1， 同时将客户拉入不诚信黑名单, 同时移除他的那条appointment
    #这里filter 可以用一个Q，比较复杂，我就写两个if了
    if Appointment.objects.filter(user_accepted="False").exists():
        listshit = list(Appointment.objects.filter(user_accepted="False").values("ssn","pid","slotid"))
        for i in listshit:
            thessn = i['ssn']
            theslotid = i['slotid']
            thepid = i['pid']
            Appointment.objects.filter(ssn = thessn).delete()
            notaccepted =Notacceptedappointment(ssn=thessn,slotid=theslotid,pid=thepid,user_accepted="False",user_canceled="pending",user_showedup="pending")
            notaccepted.save()
            thebaduser = Baduser(ssn=thessn)
            thebaduser.save()
            update_query = 'UPDATE provider_availability SET capacity = capacity + 1 WHERE pid = ? AND slotid = ?'
            cur.execute(update_query, (thepid, theslotid))
            print(cur.fetchall())
            con.commit()
    if Appointment.objects.filter(user_canceled="True").exists():
        listshit = list(Appointment.objects.filter(user_canceled="True").values("ssn","pid","slotid"))
        for i in listshit:
            thessn = i['ssn']
            theslotid = i['slotid']
            thepid = i['pid']
            Appointment.objects.filter(ssn = thessn).delete()
            cancelled = Cancelledappointment(ssn=thessn,slotid=theslotid,pid=thepid,user_accepted="True",user_canceled="True",user_showedup="pending")
            cancelled.save()
            thebaduser = Baduser(ssn=thessn)
            thebaduser.save()
            update_query = 'UPDATE provider_availability SET capacity = capacity + 1 WHERE pid = ? AND slotid = ?'
            cur.execute(update_query, (thepid, theslotid))
            print(cur.fetchall())
            con.commit()
    sql_query = '''SELECT user.ssn,provider.pid,user.priorityid,distance.distance,provider_availability.capacity,user_availability.slotid
                   FROM user,provider,distance,provider_availability,user_availability,user_travel_limit,provider_travel_limit
                   WHERE user.ssn = distance.ssn 
                        AND provider.pid = distance.pid
                        AND provider.pid = provider_availability.pid
                        AND user.ssn = user_availability.ssn
                        AND user_availability.slotid = provider_availability.slotid
                        AND provider_availability.capacity > 0
                        AND user_travel_limit.ssn = user.ssn
                        AND provider_travel_limit.pid = provider.pid
                        AND distance.distance <= user_travel_limit.distance
                        AND distance.distance <= provider_travel_limit.distance
                    ORDER BY user.priorityid ASC, distance.distance ASC
                   '''


    # sql_query2 = '''SELECT user.ssn,provider.pid,user.priorityid,distance.distance
    #                    FROM user,provider,distance,provider_availability,user_availability
    #                    WHERE user.ssn = distance.ssn
    #                         AND provider.pid = distance.pid
    #                         AND provider.pid = provider_availability.pid
    #                         AND user.ssn = user_availability.ssn
    #                         AND user_availability.slotid = provider_availability.slotid
    #                         AND provider_availability.capacity > 0
    #                     ORDER BY user.priorityid ASC, distance.distance ASC
    #                         '''
    result = cur.execute(sql_query).fetchall()
    #print the result if you want to see the viable table without triming due to provider capacity
    #print("SHIT")
    print(result)
    userhashset = []
    provider_slot_hashmap = {}
    for i in result:
        provider = i[1]
        ssn = i[0]
        priorityid = i[2]
        distance = i[3]
        providercapacity = i[4]
        slotid = i[5]


        # 如果user 已经在真实的appointment 列中(却还未确认），跳过
        if Appointment.objects.filter(ssn=ssn,user_accepted="pending").exists():
            continue
        if Appointment.objects.filter(ssn=ssn,user_accepted="True").exists():
            continue
        if Cancelledappointment.objects.filter(ssn=ssn,slotid=slotid,pid=provider).exists():
            continue
        if (provider,slotid) not in provider_slot_hashmap.keys():
            if determinebaduser(ssn):
                continue
            if ssn in userhashset:
                continue
            provider_slot_hashmap[(provider,slotid)] = providercapacity - 1
            userhashset.append(ssn)
            # Here to save this particular appointment to our appointment table
            print("SSN = " + str(ssn))
            print("provider,slot  = " + str((provider,slotid)))
            print("distance = " + str(distance))
            newappointment = Appointment(ssn=ssn,slotid=slotid,pid=provider,user_accepted="pending",user_canceled="pending",user_showedup="pending")
            newappointment.save()
        elif provider_slot_hashmap[(provider,slotid)] == 0:
            continue
        else:
            if ssn in userhashset:
                continue
            provider_slot_hashmap[(provider,slotid)] = provider_slot_hashmap[(provider,slotid)] - 1
            userhashset.append(ssn)
            print("SSN = " + str(ssn))
            print("provider  = " + str((provider,slotid)))
            print("distance = " + str(distance))
            #Here to save this particular appointment to our appointment table
            newappointment = Appointment(ssn=ssn,slotid=slotid,pid=provider,user_accepted="pending",user_canceled="pending",user_showedup="pending")
            newappointment.save()
    print(provider_slot_hashmap)
    for (provider,slotid) in provider_slot_hashmap.keys():
        print("Provider,slotid " + str((provider,slotid)) + " still have " + str(provider_slot_hashmap[(provider,slotid)]) + " chances")
        update_query = 'UPDATE provider_availability SET capacity = ? WHERE pid = ? AND slotid = ?'
        cur.execute(update_query,(provider_slot_hashmap[(provider,slotid)],provider,slotid))
        print(cur.fetchall())
        print("Executed")
        #provider_availability_object.capacity = provider_slot_hashmap[(provider,slotid)]
        #provider_availability_object.save()
        con.commit() #Be sure to commit! I spent an hour figuring out what's wrong T T
    con.close()
    return HttpResponse("Looks OK")


def providertoseeappointments(request):
    pid = request.POST.get('pid')
    data = Appointment.objects.filter(pid=pid)
    notaccepted = Notacceptedappointment.objects.filter(pid=pid)
    cancelled = Cancelledappointment.objects.filter(pid=pid)
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    update_appointment_query = 'SELECT name,Description,user_accepted,user_canceled,user_showedup FROM appointment,user,slotblock WHERE appointment.pid =? and appointment.ssn = user.ssn and appointment.slotid = slotblock.slotid'
    update_cancelledappointment_query = 'SELECT name,Description,user_accepted,user_canceled,user_showedup FROM cancelledappointment,user,slotblock WHERE cancelledappointment.pid =? and cancelledappointment.ssn = user.ssn and cancelledappointment.slotid = slotblock.slotid'
    update_declineappointment_query = 'SELECT name,Description,user_accepted,user_canceled,user_showedup FROM notacceptedappointment,user,slotblock WHERE notacceptedappointment.pid =? and notacceptedappointment.ssn = user.ssn and notacceptedappointment.slotid = slotblock.slotid'
    cur.execute(update_appointment_query, pid)
    appointmentdata = cur.fetchall()
    cur.execute(update_cancelledappointment_query, pid)
    cancelleddata = cur.fetchall()
    cur.execute(update_declineappointment_query, pid)
    declineddata = cur.fetchall()
    con.close()
    context = {"appointments":appointmentdata,"NOT_ACCEPTED":cancelleddata,"CANCELLED":declineddata}
    return render(request,'Providerwanttosee.html',context)


def tousertoseeoffer(request):
    ssn = request.POST.get('SSN')
    data = Appointment.objects.filter(ssn=ssn)
    notaccepted = Notacceptedappointment.objects.filter(ssn=ssn)
    cancelled = Cancelledappointment.objects.filter(ssn=ssn)
    context = {"appointments":data,"NOT_ACCEPTED":notaccepted,"CANCELLED":cancelled}
    return render(request,'Userwanttosee.html',context)

def tolearnprovider(request):
    pid = request.POST.get('PID')
    p1 = list(Provider.objects.filter(pid=pid).values('name','phone'))
    p2 = list(Provideraddress.objects.filter(pid=pid).values('street', 'city','state','zipcode','locationx','locationy'))
    p = []
    p.append(p1)
    p.append(p2)
    return HttpResponse(p)

def tolearntime(request):
    slotid = request.POST.get('slotid')
    timeinfo = list(Slotblock.objects.filter(slotid=slotid).values('description'))
    return HttpResponse(timeinfo)

def tocomputedistance(request):
    ssn = request.POST.get('SSN')
    pid = request.POST.get('PID')
    distance = list(Distance.objects.filter(ssn=ssn,pid=pid).values('distance'))
    return HttpResponse(distance)

def toacceptoffer(request):
    ssn = request.POST.get('SSN')
    if not Appointment.objects.filter(ssn=ssn,user_accepted='pending').exists():
        return HttpResponse("You already made your decision")
    userappointment = Appointment.objects.get(ssn = ssn)
    userappointment.user_accepted = 'True'
    userappointment.save()
    return HttpResponse("Thanks for accepting the offer!")

def todeclineoffer(request):
    ssn = request.POST.get('SSN')
    if not Appointment.objects.filter(ssn=ssn,user_accepted='pending').exists():
        return HttpResponse("You already made your decision!")
    userappointment = Appointment.objects.get(ssn = ssn)
    userappointment.user_accepted = 'False'
    userappointment.save()
    return HttpResponse("You wasted other people's time. SHAME ON YOU")

def tocanceloffer(request):
    ssn = request.POST.get('SSN')
    if Appointment.objects.filter(ssn=ssn,user_accepted='pending').exists():
        return HttpResponse("You have to first accept that offer! Dude!")
    if Appointment.objects.filter(ssn=ssn,user_accepted='False').exists():
        return HttpResponse("You already declined it, what the heck are you doing????")
    userappointment = Appointment.objects.get(ssn = ssn)
    userappointment.user_canceled = "True"
    userappointment.save()
    return HttpResponse("You wasted other people's time. YOU DESERVE TO GET COVID")

def toquery3(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_query = '''SELECT provider.pid,user.priorityid,distance.distance,provider_availability.capacity,user_availability.slotid
                   FROM user,provider,distance,provider_availability,user_availability,user_travel_limit,provider_travel_limit
                   WHERE user.ssn = 357550302
                        AND provider.pid = distance.pid
                        AND provider.pid = provider_availability.pid
                        AND user.ssn = user_availability.ssn
                        AND user_availability.slotid = provider_availability.slotid
                        AND provider_availability.capacity > 0
                        AND user_travel_limit.ssn = user.ssn
                        AND provider_travel_limit.pid = provider.pid
                        AND distance.distance <= user_travel_limit.distance
                        AND distance.distance <= provider_travel_limit.distance
                        AND user.ssn NOT in (SELECT ssn from appointment)
                    ORDER BY user.priorityid ASC, distance.distance ASC
                   '''
    cur.execute(sql_query)
    data = cur.fetchall()
    con.close()
    return HttpResponse(data)


def toquery5(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_query = '''SELECT user.ssn,user.name, slotblock.Description
                    FROM user,prioritydate,slotblock
                    WHERE user.priorityid = prioritydate.priorityid
                    AND prioritydate.slotid = slotblock.slotid
    '''
    cur.execute(sql_query)
    data = cur.fetchall()
    con.close()
    return HttpResponse(data)

def toquery6(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_query = '''SELECT ssn
                    FROM cancelledappointment
                    group by ssn
                    having count(*) >= 3
    '''
    cur.execute(sql_query)
    data1 = cur.fetchall()
    sql_query = '''SELECT ssn
                    FROM appointment
                    WHERE user_showedup = "False"
                    group by ssn
                    having count() >= 2
    '''
    cur.execute(sql_query)
    data2 = cur.fetchall()
    listofdata = [data1,data2]
    con.close()
    return HttpResponse(listofdata)


def toquery7(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_query = '''SELECT provider.pid, name
                    FROM provider, appointment
                    WHERE provider.pid=appointment.pid
                    AND user_showedup = "True"
                    GROUP BY provider.pid, name
                    ORDER BY COUNT(*) DESC
                    LIMIT 1
    '''
    cur.execute(sql_query)
    data = cur.fetchall()
    con.close()
    return HttpResponse(data)
