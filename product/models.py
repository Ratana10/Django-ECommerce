from django.db import models

# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm



class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name = 'children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
        
    # def __str__(self):
    #     print(f'testing1: {self.parent}')
    #     return self.title   
    
    class MPTTMeta:
        order_insertion_by = ['title']
        
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        return self.title   
    # def __str__(self):
    #     full_path = [self.title]
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.title)
    #         k = self.parent
    #     return ' / '.join(full_path[::-1])
            
        
    
class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    #one to many  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)# one product have one category -> one category have many product
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', null=True)
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
     
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" width="100px"/>'.format(self.image.url))
    

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" width="100px"/>'.format(self.image.url))
    


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=50, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
    
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']    
        
    


    

    
