from django import forms
from product.models import Comment
from django.forms import ModelForm


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()
    
    

    
    