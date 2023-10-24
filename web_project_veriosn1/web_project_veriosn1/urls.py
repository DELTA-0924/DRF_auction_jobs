
from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from app.views import *
from django.urls import path

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('signin', SignInView.as_view(), name='signin'),

    path('userlist',UserlistView.as_view(),name='userlist'),
    path('admin',admin.site.urls)
]
from rest_framework.authtoken import views
urlpatterns += [
    path('api-token-auth', views.obtain_auth_token)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)