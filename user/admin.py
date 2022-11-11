from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address','phone','city', 'country', 'image_tag']
    
    
admin.site.register(UserProfile, UserProfileAdmin)
