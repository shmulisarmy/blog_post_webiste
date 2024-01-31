# forms.py
from django import forms

class make_post(forms.Form):
    # Define your form fields here
    text = forms.CharField(widget=forms.TextInput())
    # Add more fields as needed

class make_comment(forms.Form):
    # Define your form fields here
    text = forms.CharField(widget=forms.TextInput())
    # Add more fields as needed
