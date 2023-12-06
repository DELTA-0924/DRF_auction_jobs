from pyexpat import model
from rest_framework import serializers
from rest_framework.views import Response
from .models import *
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
        
class EmpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')        
        
# Создание польвателя         
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','email','role','avatar')
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            avatar=validated_data['avatar']
        )
        user.set_password(validated_data['password'])  # Эта строка хеширует пароль
        user.save()    
        return user
    def validate_username(self, value):
        # Пример пользовательской проверки для поля username
        if len(value)> 8 or len(value)<3:
            raise serializers.ValidationError("Имя пользователя должно содержать не менее 3 символов и не более 8 символов.")
        return value
        
#Auctions serializers
class AuctionCreateSerializer(serializers.ModelSerializer):
    creator=serializers.HiddenField(default=serializers.CurrentUserDefault)
    class Meta:
        model=CustomAuction
        fields='__all__'
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomAuction
        fields='__all__'
        
#Task serializers
class TaskCreatorSerializer(serializers.ModelSerializer):
    student=serializers.HiddenField(default=serializers.CurrentUserDefault)
    class Meta:
        model=CustomTask
        fields='_all_'
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomTask
        fields='__all__'


     