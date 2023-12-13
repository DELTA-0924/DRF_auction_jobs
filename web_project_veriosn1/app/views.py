
import re
from rest_framework.decorators import permission_classes
from django.contrib.sessions.models import Session
from django.utils import timezone
from statistics import quantiles
from django.contrib.auth import login, logout
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .models import CustomAuction, CustomTask, CustomUser
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .permissions import IsEmployer,IsLogin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .paginations import *
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from django.shortcuts import get_object_or_404

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 
from .consumers import *


class UserDetailsView(APIView):
    permission_classes = [IsLogin,IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,JSONParser)
 
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
  
    def post(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SignUpView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer 
    parser_classes = (MultiPartParser, FormParser, JSONParser) 
    user=CustomUser
    tokenkey=''
    def create(self, request, *args, **kwargs):
        role = "Student"
        data_copy = request.data.copy()
        data_copy['role'] = role         
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)           
        return Response({"Userdata":self.user,"Token":self.tokenkey} , status=status.HTTP_201_CREATED) 
        
    def perform_create(self, serializer):
        user = serializer.save()  # Сохраните пользователя
        token, created = Token.objects.get_or_create(user=user)        
        token.save() 
        login(self.request, user)
        self.user=serializer.data;
        self.tokenkey=token.key;
        print(token.key)
        return Response({"Userdata":self.user,"Token":self.tokenkey}, status=status.HTTP_201_CREATED) 

class EmplSignUpView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = UserCreateSerializer
    user=CustomUser
    tokenkey=''
    parser_classes = (MultiPartParser, FormParser,JSONParser) 
    def create(self, request, *args, **kwargs):
        role = "Employer"
        data_copy = request.data.copy()
        data_copy['role'] = role  
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"Userdata":self.user,"Token":self.tokenkey}, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):
        user = serializer.save()
        #Token.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        token.save() 
        login(self.request, user)
        self.user=serializer.data;
        self.tokenkey=token.key;
        print(token.key)
        return Response({"Userdata":self.user,"Token":self.tokenkey}, status=status.HTTP_201_CREATED) 


class SignInView(APIView):
    def post(self, request, *args, **kwargs):   
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):  
            if not user.is_session_active:  # Проверка активности аккаунта пользователя
                user.is_session_active = True  # Устанавливаем флаг активной сессии
                user.save()
                login(request, user)
                token, created = Token.objects.get_or_create(user=user) 
                context = {'Userdata': request.user.username, 'Token': token.key}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Аккаунт пользователя  активен'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)           

        
class SignOutView(APIView):
    def post(self, request, *args, **kwargs):
        token_key = request.data.get('Token')  # Предположим, что токен передается в теле запроса
        try:
            token = Token.objects.get(key=token_key)
            user = CustomUser.objects.get(pk=token.user_id) 
            user.is_session_active = False
            user.save()
            # Используйте user для нужных действий с пользователем
            return Response({'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Токен не найден'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

class UserSearchAPIView(APIView):
    def get (self, request, pk, format=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserGetSerilizer(user)  # Замените на ваш сериализатор для пользователя
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuctionCreateView(generics.CreateAPIView):
    serializer_class = AuctionCreateSerializer
   # permission_classes = (IsEmployer,IsLogin)

    def perform_create(self, serializer):
        user_creator = self.request.user.username  # Получаем имя пользователя
        active="False"
        serializer.save(user_creator=user_creator,active=active)  # Сохраняем имя пользователя в user_creator

class AuctionListView(generics.ListAPIView):
    #permission_classes = (IsAuthenticated, IsEmployer,)
    serializer_class = AuctionSerializer
    pagination_class = AuctionlistPagination

    def get_queryset(self):
         return CustomAuction.objects.all()  # Замените это на ваш запрос к базе данных для получения объектов CustomAuction

class AuctionDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            auction = CustomAuction.objects.get(pk=pk)
            print(auction.auctionId)
            tasks = CustomTask.objects.filter(auction=auction.auctionId)
            ratings=CustomRating.objects.filter(auction=auction.auctionId)
        except CustomAuction.DoesNotExist:
            return Response({"error": "Что-то пошло не так"}, status=status.HTTP_404_NOT_FOUND)
        auction_serializer = AuctionSerializer(auction)
        if   len(tasks)!=0:          
            tasks_serializer = TaskSerializer(tasks, many=True)
            if len(ratings)==0:
                context={"students":tasks_serializer.data,"rating":None}                
                response_data = {
                "auction": auction_serializer.data,
                "tasks": context 
                }
            else:
                rating_serializer=CustomRatingSerializer(ratings,many=True)
                sorted_ratings = sorted(rating_serializer.data, key=lambda x: x.get('point', 0), reverse=True)
                context={"students":tasks_serializer.data,"rating":sorted_ratings}
                response_data = {
                "auction": auction_serializer.data,
                "tasks": context
                
            }
            return Response(response_data, status=status.HTTP_200_OK)        
        response_data = {
            "auction": auction_serializer.data,
            "tasks": None
        }
        return Response(response_data, status=status.HTTP_200_OK)


class AuctionEdit(generics.UpdateAPIView):
    queryset = CustomAuction.objects.all()
    serializer_class = AuctionCreateSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.queryset, pk=pk)

    #def perform_update(self, serializer):
    #    instance = serializer.save()
    #    channel_layer = get_channel_layer()
    #    async_to_sync(channel_layer.group_send)(
    #        "auction_edit_update",  # Укажите имя группы для рассылки
    #        {
    #            "type": "notify_data_update",
    #            "text": "Данные были обновлены",  # Ваше уведомление
    #        }
    #    )

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreatorSerializer

    def create(self, request, *args, **kwargs):
        auction_id = kwargs.get('pk')
        auction = get_object_or_404(CustomAuction, pk=auction_id)
        
        if auction:
            task_data = {
                'auction': auction_id,
                'task': request.data.get('task')
                
            }
            serializer = self.get_serializer(data=task_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'CustomAuction not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):                
        serializer.save(
            user_creator=self.request.user.username ,
            email=self.request.user.email
        )

class TaskListView(generics.ListAPIView):
    queryset=CustomTask.objects.all()
    serializer_class=TaskSerializer
 #  permission_classes=(IsAuthenticatedOrReadOnly,IsLogin)
   # pagination_class=Tasklistagination

class GetUserToken(APIView):
    def post(self, request, format=None):
        # Предполагается, что запрос содержит данные для аутентификации пользователя,
        # например, его имя пользователя и пароль.
        username = request.data.get('username')
        password = request.data.get('password')
     
        print(username,password,sep='\n')
        # Попробуем аутентифицировать пользователя
        user = CustomUser.objects.filter(username=username).first()
        
        print(user.username,user.password,user.id,sep='\n')
        if user  and user.check_password(password):           
           token, created = Token.objects.get_or_create(user=user)
           return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

class UserlistView(generics.ListAPIView):
    
    queryset=CustomUser.objects.all();
    serializer_class=UserSerializer    

class CustomRatingCreateView(generics.CreateAPIView):
    serializer_class = CustomRatingSerializer
    def post(self, request, pk):
        auction_id = pk
        uchastnik = request.data.get('uchastnik')
        point=request.data.get('point')
        rating={
            "auction":auction_id,
            "uchastnik":uchastnik,
            "point":point
            }
        serializer = self.get_serializer(data=rating)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)            
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):                
        serializer.save()

class RatingDeleteView(generics.DestroyAPIView):
    def delete(self, request,pk,pk2):
        rating_id=pk2
        obj_to_delete=CustomRating.objects.get(ratingID=rating_id)
        if obj_to_delete:
            obj_to_delete.delete()
            return Response("succes delete",status=status.HTTP_200_OK)
        return Response("unsucces delete",status=status.HTTP_404_NOT_FOUND)

class AuctionDeleteView(generics.DestroyAPIView):
    def delete(self, request,pk):
        auction_id=pk
        obj_to_delete=CustomAuction.objects.get(auctionId=auction_id)
        if obj_to_delete:
            obj_to_delete.delete()
            return Response("succes delete",status=status.HTTP_200_OK)
        return Response("unsucces delete",status=status.HTTP_404_NOT_FOUND)

class TaskDeleteView(generics.DestroyAPIView):
    def delete(self, request,pk,pk2):
        task_id=pk2
        obj_to_delete=CustomTask.objects.get(taskId=task_id)
        if obj_to_delete:
            obj_to_delete.delete()
            return Response("succes delete",status=status.HTTP_200_OK)
        return Response("unsucces delete",status=status.HTTP_404_NOT_FOUND)
