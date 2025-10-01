from django import forms
# Import widgets to specifically set input type and attributes
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

# Form for user sign-in
class UserSignInForm(forms.Form):
    # 1. Define the Username Field
    username = forms.CharField(
        label=False, # We don't want a label displayed, as the placeholder is sufficient
        widget=TextInput(attrs={
            # Add the CSS class for styling
            'class': 'form-control', 
            # Add the placeholder text
            'placeholder': 'Username or Email' 
        })
    )
    
    # 2. Define the Password Field
    password = forms.CharField(
        label=False,
        widget=PasswordInput(attrs={
            # Add the CSS class for styling
            'class': 'form-control', 
            # Add the placeholder text
            'placeholder': 'Password' 
        })
    )

# Form for user creation (Sign Up) with custom styling
class MyUserCreationForm(UserCreationForm):
    # Add email field
    email = forms.EmailField(
        required=True,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']

    # Override __init__ to apply the 'form-control' class and custom placeholders
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply default styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })
            
        # Set specific placeholders for better user experience
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user