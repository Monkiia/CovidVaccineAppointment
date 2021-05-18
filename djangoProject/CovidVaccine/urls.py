from django.urls import path

from CovidVaccine import views

urlpatterns = [
    path('', views.tocovidvaccine),
    path('UserLogin',views.touserlogin),
    path('ProviderLogin',views.toproviderlogin),
    path('UserAPI',views.touserapi),
    path('ProviderAPI',views.toproviderapi),
    path('UserRegister',views.touserregister),
    path('ProviderRegister',views.toproviderregister),
    path('ProviderSchedule',views.toproviderschedule),
    path('UserRegisterDataInput',views.touserregisterdatainput),
    path('help',views.tohelp),
    path('UserSchedule',views.touserschedule),
    path('tocreateormodifyschedule',views.updateuserschedule),
    path('provideraddschedule',views.providertoaddschedule),
    path('asynchronous_calculate_and_update',views.calculate_and_update),
    path('ProviderSeeAppointments',views.providertoseeappointments),
    path('Usertoseeappointmentoffer',views.tousertoseeoffer),
    path('LearnProvider',views.tolearnprovider),
    path('LearnTime',views.tolearntime),
    path('ComputeDistance',views.tocomputedistance),
    path('AcceptOffer',views.toacceptoffer),
    path('DeclineOffer',views.todeclineoffer),
    path('CancelOffer',views.tocanceloffer),
    path('Query3',views.toquery3),
    path('Query5', views.toquery5),
    path('Query6', views.toquery6),
    path('Query7', views.toquery7)
]
