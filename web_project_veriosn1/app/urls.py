
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app.views import *
from django.urls import path,re_path
from rest_framework import permissions



urlpatterns = [
   #registration
    path('student-signup', SignUpView.as_view(), name='signup'),
    path('employer-signup', EmplSignUpView.as_view(), name='signup'),
    #login
    path('signin', SignInView.as_view(), name='signin'),
    #logout
    path('signout', SignOutView.as_view(), name='signout'),
    
    path("task-create",TaskCreateView.as_view(),name="task-create"),
    path("auction-create",AuctionCreateView.as_view(),name="auction-create"),
    path("auction-edit/<int:pk>",AuctionEdit.as_view(),name="auction-edit"),
    path("auction-detail/<int:pk>", AuctionDetail.as_view(),name="auction-detail"),
    path("auction-edit/<int:pk>/auction-delete",AuctionDeleteView.as_view(),name="auction-delete"),
    
    path("auction-detail/<int:pk>/task-create",TaskCreateView.as_view(),name="task-create"),
    path("auction-detail/<int:pk>/task-delete/<int:pk2>",TaskDeleteView.as_view(),name="task-delete"),



    path("auction-detail/<int:pk>/rating-add",CustomRatingCreateView.as_view(),name="rating-create"),
    path("auction-detail/<int:pk>/rating-sub/<int:pk2>",RatingDeleteView.as_view(),name="rating-sub"),
    

    path("auction-list",AuctionListView.as_view(),name="auction-list"),
    path("task-list",TaskListView.as_view(),name="task-list"),

    
    path("search-student/<int:pk>",UserSearchAPIView.as_view(),name="search"),
    


    
    #Users details
    path('userlist',UserlistView.as_view(),name='userlist'),
    path('profile', UserDetailsView.as_view(), name='profile'),
    path('get-token', GetUserToken.as_view(),name="get-token"),
]