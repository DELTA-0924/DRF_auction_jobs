from pyexpat import model
from rest_framework import serializers
from rest_framework.views import Response
from .models import *
from datetime import datetime
#Users serialiazers
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser;
        fields="__all__"
#Инкапсуляция модели пользвателя
     
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields ='__all__'

class UserGetSerilizer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ('id', 'password', 'username', 'first_name', 'last_name', 'location', 'skills', 'salary', 'about', 'years_old', 'speciality', 'avatar', 'email', 'role')

        
class EmpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')        
        
# Создание польвателя         
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','email','role')
    def create(self, validated_data):        
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],    
        )
        user.set_password(validated_data['password'])  # Эта строка хеширует пароль
        user.save()    
        return user
    def validate_username(self, value):
        # Пример пользовательской проверки для поля username
        if len(value)> 20 or len(value)<3:
            raise serializers.ValidationError("Имя пользователя должно содержать не менее 3 символов и не более 8 символов.")
        return value
        
#Auctions serializers
class AuctionCreateSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CustomAuction
        fields = ('titelname', 'task', 'active', 'max_interns', 'min_interns', 'start_date', 'end_date', 'creator', 'user_creator')

    def create(self, validated_data):
        now = datetime.now()
        validated_data['start_date'] = now.strftime("%d-%H-%M")
        return super().create(validated_data)

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomAuction
        fields = ('auctionId','titelname', 'task', 'active', 'max_interns', 'min_interns', 'start_date', 'end_date', 'creator','user_creator')
        
#Task serializers
class TaskCreatorSerializer(serializers.ModelSerializer):
    student=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=CustomTask
        fields='__all__'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomTask
        fields='__all__'


class CustomRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomRating
        fields = ('ratingID', 'auction', 'uchastnik','point')