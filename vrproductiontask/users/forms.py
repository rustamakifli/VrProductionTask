from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from users.models import Contact

USER = get_user_model()

class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = (
            "first_name",
            "last_name",
            'email',
            'birthdate',
            'sex',
        )
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'First Name here'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Last Name here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'single-input',
                'placeholder': 'Email Address'
            }),
            'birthdate': forms.DateInput(attrs={
                'placeholder':'Birth Date', 
                'class': 'single-input',
                'type': 'date',                                                                 
            }),
            'sex': forms.Select(attrs={
                'placeholder':'MR or MRs', 
                'class': 'single-input', 
            }),
        }
    

class LoginForm(AuthenticationForm):
    class Meta:
        model = USER
        fields = (
            'username',
            'password',
        )
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 
    'class': 'single-input',
        'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'single-input',
        'placeholder': 'Password'
    }))

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'single-input',
                'placeholder': 'Confirm Password'
            }))

    class Meta:
        model = USER
        fields = (
            'username',
            "first_name",
            "last_name",
            "image",
            'email',
            'password',
            'confirm_password',
            'birthdate',
            'sex',
        )

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Username here'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'First Name here'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Last Name here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'single-input',
                'placeholder': 'Email Address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Phone Number'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'single-input',
                'placeholder': 'Password'
            }),
            'sex': forms.Select(attrs={
                'placeholder':'MR or MRs', 
                'class': 'single-input', 
            }),
            'birthdate': forms.DateInput(attrs={
                'placeholder':'Birth Date', 
                'class': 'single-input',
                'type': 'date',                                                                 
            })
        }

    def clean(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError("Please make sure your passwords match")
        return super().clean()
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'name',
            'email',
            'subject',
            'message',
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Name here'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'single-input',
                'placeholder': 'Email here'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'single-input',
                'placeholder': 'Subject here'
            }),
            'message': forms.Textarea(attrs={
                'cols': 40,
                'rows': 5,
                'placeholder': 'Message here'
            })
        }