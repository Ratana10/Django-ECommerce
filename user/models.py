from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=20, blank=True)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name+' '+self.user.last_name+' ['+self.user.username+'] '
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" width="100px"/>'.format(self.image.url))
    
    image_tag.short_description ='Image'
    
