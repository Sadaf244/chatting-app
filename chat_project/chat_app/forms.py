from django import forms
from .models import ChatUser, Interest

class SignupForm(forms.ModelForm):
    
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all().distinct(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = ChatUser
        fields = ['full_name', 'email', 'phone', 'gender', 'country', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }