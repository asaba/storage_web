# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    def backendused(self):
        backends = []
        for g in AuthUserGroups.objects.all().filter(user=self):
            for p in BackendUsed.objects.all().filter(project_name=g.group.name):
                if p.backend not in backends:
                    backends.append(p.backend)
        return backends

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class History(models.Model):
    idhistory = models.IntegerField(db_column='id')
    filename = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'history'


class Login(models.Model):
    idlogin = models.IntegerField(primary_key=True, db_column='id')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    mjd_start = models.FloatField()
    mjd_stop = models.FloatField()

    class Meta:
        managed = False
        db_table = 'login'


class SetupHistory(models.Model):
    idsetuphistory = models.IntegerField(db_column='id')
    backend = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    project = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    lo = models.CharField(max_length=255)
    project_dir = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'setup_history'


class SsLogin(models.Model):
    username = models.CharField(max_length=64)
    idsslogin = models.CharField(primary_key=True, max_length=64, db_column='id')
    mjd_start = models.FloatField()
    mjd_stop = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ss_login'


class Tdays(models.Model):
    idtdays = models.IntegerField(db_column='id')
    filename = models.CharField(unique=True, max_length=255, verbose_name="Download")
    date = models.CharField(max_length=32, blank=True, verbose_name="Date (UTC)")
    source = models.CharField(max_length=32, blank=True)
    project_name = models.CharField(db_column='Project_Name', max_length=255, blank=True)  # Field name made lowercase.
    telescope = models.CharField(max_length=32, blank=True)
    mjd_start = models.FloatField(blank=True, null=True)
    mjd_stop = models.FloatField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True, verbose_name="freq (MHz)")
    bandwidth = models.FloatField(blank=True, null=True, verbose_name="bandwidth (MHz)")
    localoscillator = models.FloatField(blank=True, null=True, verbose_name="local oscillator (MHz)")
    samplerate = models.FloatField(blank=True, null=True, verbose_name="Samplerate (Hz)")
    receiver = models.CharField(max_length=32)
    backend = models.CharField(max_length=32)
    project_dir = models.CharField(max_length=255)
    schedulename = models.CharField(db_column='ScheduleName', max_length=255)  # Field name made lowercase.
    source_ra = models.FloatField(verbose_name="Source Ra (deg)")
    source_dec = models.FloatField(verbose_name="Source Dec (deg)")

    class Meta:
        managed = False
        db_table = 'tdays'


class BackendUsed(models.Model):
    id = models.IntegerField(primary_key=True)
    project_name = models.CharField(db_column='Project_Name', max_length=255, blank=True)  # Field name made lowercase.
    backend = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'backend_used'  # your view name
