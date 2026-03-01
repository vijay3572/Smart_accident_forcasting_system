from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    # ✅ extra validation (same email twice avoid)
    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    # ✅ make sure email/first/last saved
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower().strip()
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import AccidentReport

class AccidentReportForm(forms.ModelForm):
    class Meta:
        model = AccidentReport
        fields = ['vehicle_type', 'location', 'latitude', 'longitude', 'notes', 'image']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
from django import forms
from .models import AccidentReport

class AccidentReportForm(forms.ModelForm):
    class Meta:
        model = AccidentReport
        fields = ['vehicle_type', 'location', 'latitude', 'longitude', 'notes', 'image']

        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AccidentReportForm(forms.ModelForm):
    class Meta:
        model = AccidentReport
        fields = [
            'name',
            'mobile',
            'vehicle_number',
            'vehicle_type',
            'location',
            'latitude',
            'longitude',
            'notes',
            'image',
            'video'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),

            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }
