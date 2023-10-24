from msilib.schema import CustomAction
from statistics import quantiles
from django.contrib.auth import login
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .models import CustomAuction, CustomTask, CustomUser
from .serializer import AuctionCreateSerializer, AuctionSerializer, EmpUserSerializer, TaskCreatorSerializer, TaskSerializer, UserCreateSerializer,UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .permissions import IsEmployer
class SignUpView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        role = "Student"
        request.data['role'] = role  
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

   
        login(self.request, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EmplSignUpView(generics.CreateAPIView):
    queryset = CustomUser
    serializer_class = EmpUserSerializer

    def create(self, request, *args, **kwargs):
        role = "Employer"
        request.data['role'] = role 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

        
        login(self.request, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(SignInView, self).post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.user  # Подразумевается, что user доступен после успешной аутентификации
            login(request, user)
        return response
    
class UserlistView(generics.ListCreateAPIView):
    queryset=CustomUser.objects.all();
    serializer_class=UserSerializer    
 
    permission_classes = (IsAuthenticated,IsEmployer)


class AuctionCreateView(generics.CreateAPIView):
    queryset=CustomAuction
    serializer_class=AuctionCreateSerializer
    permission_classes = (IsAuthenticated,)
    
class AuctionListView(generics.ListAPIView):
    queryset=CustomAuction
    serializer_class=AuctionSerializer;
    permission_classes=(IsAuthenticatedOrReadOnly,)
class TaskCreateView(generics.CreateAPIView):
    queryset=CustomTask.objects.all()
    serializer_class=TaskCreatorSerializer
    permission_classes = (IsAuthenticated,)

class TaskListView(generics.ListAPIView):
    queryset=CustomTask.objects.all()
    serializer_class=TaskSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)






