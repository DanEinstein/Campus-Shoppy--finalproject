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
    class Meta:
        model = User
        # 'username' is the only field you need to specify here; 
        # password1 and password2 are automatically included by UserCreationForm.
        fields = ['username']

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
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'