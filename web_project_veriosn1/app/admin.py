from django.contrib import admin
from .models import *

admin.site.register(CustomUser) 
admin.site.register(CustomAuction) 
admin.site.register(CustomRating) 
admin.site.register(CustomTask) 