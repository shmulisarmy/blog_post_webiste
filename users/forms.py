from django import forms

class signup_form(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    password = forms.CharField()

class login_form(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    password = forms.CharField()
