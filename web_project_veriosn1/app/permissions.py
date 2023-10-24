
from urllib import request
from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
         return request.user.role=="Employer"