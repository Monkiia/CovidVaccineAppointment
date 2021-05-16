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
    path('provideraddschedule',views.providertoaddschedule)
]
