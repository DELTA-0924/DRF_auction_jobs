
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from app.views import *
from django.urls import path
urlpatterns = [
    #registration
    path('signup', SignUpView.as_view(), name='signup'),
    path('signup1', EmplSignUpView.as_view(), name='signup'),
    #login
    path('signin', SignInView.as_view(), name='signin'),
    #logout
    path('signout', SignOutView.as_view(), name='signout'),
    
    path("task-create",TaskCreateView.as_view(),name="task-create"),
    path("auction-create",AuctionCreateView.as_view(),name="auction-create"),
    

    path("auction-list",AuctionListView.as_view(),name="auction-list"),
    
    path("search-student/<int:pk>",UserSearchAPIView.as_view(),name="search"),
    


    
    #Users details
    path('userlist',UserlistView.as_view(),name='userlist'),
    path('profile', UserDetailsView.as_view(), name='profile'),
    
    path('admin',admin.site.urls)
]
from rest_framework.authtoken import views
urlpatterns += [
    path('get-token', GetUserToken.as_view(),name="get-token")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)