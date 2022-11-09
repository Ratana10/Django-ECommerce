from django.db import models

# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel



class Category(models.Model):
    
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name = 'children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
  
    

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
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = RichTextUploadingField()
    slug = models.SlugField()
    status = models.CharField(max_length=10, choices=STATUS)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        from django.utils.html import mark_safe
        return mark_safe(f'<p>{self.image}</p>')

    image_tag.short_description = 'Image'

    #method to create a fake table field in read only mode
    # def image_tag(self):
    #     return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    
    
    # image_tag.short_description = 'Image'
    


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    
    def __str__(self):
        return self.title
    



