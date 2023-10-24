from rest_framework import serializers
from .models import *
#Users serialiazers
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ( 'username', 'email')
class EmpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password','email')
        
#Auctions serializers
class AuctionCreateSerializer(serializers.ModelSerializer):
    creator=serializers.HiddenField(default=serializers.CurrentUserDefault)
    class Meta:
        model=CustomAuction
        fields='__all__'
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomAuction
        fealds='__all__'
        
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
        