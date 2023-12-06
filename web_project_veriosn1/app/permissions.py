
from urllib import request
from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         return bool(request.user and request.user.is_authenticated and request.user.role=="Employer")
    
class IsLogin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         return bool(request.user and request.user.is_authenticated and request.user.is_session_active==True)    