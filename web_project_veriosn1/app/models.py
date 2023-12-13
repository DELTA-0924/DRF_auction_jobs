
from asyncio import Task
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser,PermissionsMixin
from django.forms import CharField, DateField, DateTimeField, IntegerField
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.utils import timezone

class CustomUser(AbstractUser,PermissionsMixin):
    location = models.CharField(max_length=255,null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    years_old = models.IntegerField(default=16,null=True, blank=True)
    speciality = models.CharField(max_length=255,null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.EmailField(blank=True)
    role=models.CharField(max_length=10,blank=True,null=True)
    is_session_active = models.BooleanField(default=False)
    def get_auth_token(self):
        try:
                return self.auth_tokens.get()  # Получить токен пользователя
        except Token.DoesNotExist:
            return None
    def __str__(self):
        return self.username

    
class CustomAuction(models.Model):
    auctionId=models.AutoField(primary_key=True)
    titelname=models.CharField(max_length=50)
    task=models.TextField()
    active=models.BooleanField(default=0)
    max_interns=models.IntegerField()
    min_interns=models.IntegerField()
    start_date=models.CharField(max_length=50,null=True, blank=True)
    end_date=models.CharField(max_length=50,null=True, blank=True)
    creator=models.ForeignKey(CustomUser,verbose_name="Создатель",on_delete=models.PROTECT)
    user_creator=models.CharField(max_length=255,null=True, blank=True)
class CustomTask(models.Model):
    auction=models.ForeignKey(CustomAuction,verbose_name="Аукцион",on_delete=models.PROTECT,null=True,blank=True)
    taskId=models.AutoField(primary_key=True)
    task=models.TextField(); 
    student=models.ForeignKey(CustomUser,verbose_name="Студент",on_delete=models.PROTECT)
    user_creator=models.CharField(max_length=255,null=True, blank=True)
    time_send=models.DateTimeField(default=timezone.now)
    email=models.EmailField(null=True,blank=True);



class CustomRating(models.Model):
    ratingID=models.AutoField(primary_key=True)
    auction=models.ForeignKey(CustomAuction,verbose_name="Аукцион",on_delete=models.PROTECT,null=True,blank=True)    
    uchastnik=models.CharField(max_length=255,null=True, blank=True)
    point=models.IntegerField(default=0);