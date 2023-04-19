# from pyexpat import model
# from re import U
# from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['username'].disable = True
            self.fields['email'].disable = True
            self.fields['special_user'].disable = True
            self.fields['is_author'].disable = True
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 
                    'last_name', 'special_user', 'is_author')

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')