
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
from .serializer import AuctionCreateSerializer, AuctionSerializer, EmpUserSerializer, ProfileSerializer, TaskCreatorSerializer, TaskSerializer, UserCreateSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .permissions import IsEmployer,IsLogin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .paginations import *
from rest_framework.parsers import MultiPartParser, FormParser

class UserDetailsView(APIView):
    permission_classes = [IsLogin,IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
 
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
    parser_classes = (MultiPartParser, FormParser) 
    def create(self, request, *args, **kwargs):
        role = "Student"
        data_copy = request.data.copy()
        data_copy['role'] = role         
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)      
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
        
    def perform_create(self, serializer):
        user = serializer.save()  # Сохраните пользователя
        token, created = Token.objects.get_or_create(user=user)        
        token.save() 
        login(self.request, user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class EmplSignUpView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = UserCreateSerializer
    parser_classes = (MultiPartParser, FormParser) 
    def create(self, request, *args, **kwargs):
        role = "Employer"
        data_copy = request.data.copy()
        data_copy['role'] = role  
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
    def perform_create(self, serializer):
        user = serializer.save()
        #Token.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        token.save() 
        login(self.request, user)

class SignInView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')           
        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):  
            login(request, user)
            if request.user.is_authenticated:
                if not user.is_session_active:  # Проверка активности аккаунта пользователя
                    user.is_session_active = True  # Устанавливаем флаг активной сессии
                    user.save()
                    return Response({'success': 'Вы успешно вошли','username':request.user.username}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Аккаунт пользователя  активен'}, status=status.HTTP_200_OK)
            else: 
                return Response({'error': 'Аккаунт не авторизовался'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        

class SignOutView(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        if  request.user.is_authenticated :  # Проверяем аутентификацию и флаг активной сессии
            user.is_session_active = False  # Устанавливаем флаг неактивной сессии при выходе
            user.save()
            context={'useranme':request.user.username,'success': 'Вы успешно вышли'}
            logout(request)  # Выход пользователя
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Пользователь не аутентифицирован или уже вышел','username':request.user.username}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchAPIView(APIView):
    def post(self, request, pk, format=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)  # Замените на ваш сериализатор для пользователя
        return Response(serializer.data, status=status.HTTP_200_OK)

class AuctionCreateView(generics.CreateAPIView):
    queryset=CustomAuction
    serializer_class=AuctionCreateSerializer    
    permission_classes = (IsEmployer,IsLogin)
    

class AuctionListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsEmployer,)
    serializer_class = AuctionSerializer
    pagination_class = AuctionlistPagination

    def get_queryset(self):
        return CustomAuction.objects.all()  # Замените это на ваш запрос к базе данных для получения объектов CustomAuction

    


class TaskCreateView(generics.CreateAPIView):
    queryset=CustomTask.objects.all()
    serializer_class=TaskCreatorSerializer
    permission_classes = (IsAuthenticated,IsLogin)

class TaskListView(generics.ListAPIView):
    queryset=CustomTask.objects.all()
    serializer_class=TaskSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,IsLogin)
    pagination_class=Tasklistagination

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
    permission_classes = (IsAuthenticated,IsLogin,)
    queryset=CustomUser.objects.all();
    serializer_class=UserSerializer    
    pagination_class=UserlistPagination


