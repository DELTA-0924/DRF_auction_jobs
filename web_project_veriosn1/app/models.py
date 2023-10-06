from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.translation import gettext_lazy as _
import django
print(django.get_version())
class Model(models.Model):
    id = models.AutoField(primary_key=True)  
    fio = models.CharField(max_length=255)
    def __str__(self):
        return self.username
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)  
    fio = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    skills = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    about = models.TextField()
    year = models.IntegerField()
    speciality = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    accountStatus = models.BooleanField(default=True)
    accountStatus1 = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='customuser_set')

    def __str__(self):
        return self.username