# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Distance(models.Model):
    ssn = models.IntegerField()
    pid = models.IntegerField()
    distance = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'distance'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Prioritydate(models.Model):
    priorityid = models.IntegerField()
    slotid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prioritydate'


class Provider(models.Model):
    name = models.CharField(max_length=20)
    phone = models.IntegerField()
    pid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provider'


class ProviderAvailability(models.Model):
    pid = models.IntegerField()
    slotid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provider_availability'


class ProviderTravelLimit(models.Model):
    pid = models.IntegerField()
    distance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provider_travel_limit'


class ProviderWeekLock(models.Model):
    pid = models.IntegerField()
    week = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provider_week_lock'


class Provideraddress(models.Model):
    street = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    locationx = models.IntegerField()
    locationy = models.IntegerField()
    pid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'provideraddress'


class Timeblock(models.Model):
    description = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timeblock'


class User(models.Model):
    name = models.CharField(max_length=20)
    ssn = models.IntegerField()
    age = models.CharField(max_length=20)
    phone = models.IntegerField()
    priorityid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class UserAvailability(models.Model):
    ssn = models.IntegerField()
    slotid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_availability'


class UserTravelLimit(models.Model):
    ssn = models.IntegerField()
    distance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_travel_limit'


class Useraddress(models.Model):
    street = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    locationx = models.IntegerField()
    locationy = models.IntegerField()
    ssn = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'useraddress'


class Userlogin(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    ssn = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userlogin'
