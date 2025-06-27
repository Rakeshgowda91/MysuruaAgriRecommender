# crop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Soildata, Profile

class SoilDataForm(forms.ModelForm):
    # Use a ChoiceField to present a dropdown list of soil types to the user.
    SOIL_TYPE_CHOICES = [
        ('Red', 'Red'),
        ('Black', 'Black'),
        ('Loamy', 'Loamy'),
    ]
    soil_type = forms.ChoiceField(choices=SOIL_TYPE_CHOICES)

    # Use explicit field definitions with input limits and custom error messages
    nitrogen = forms.FloatField(
        required=True,
        min_value=70,
        max_value=120,
        error_messages={'required': 'Please enter a value for Nitrogen.', 'min_value': 'Value must be at least 70.', 'max_value': 'Value must be at most 120.'}
    )
    phosphorus = forms.FloatField(
        required=True,
        min_value=25,
        max_value=65,
        error_messages={'required': 'Please enter a value for Phosphorus.', 'min_value': 'Value must be at least 25.', 'max_value': 'Value must be at most 65.'}
    )
    potassium = forms.FloatField(
        required=True,
        min_value=20,
        max_value=60,
        error_messages={'required': 'Please enter a value for Potassium.', 'min_value': 'Value must be at least 20.', 'max_value': 'Value must be at most 60.'}
    )
    ph = forms.FloatField(
        required=True,
        min_value=5.5,
        max_value=6.9,
        error_messages={'required': 'Please enter a value for pH.', 'min_value': 'Value must be at least 5.5.', 'max_value': 'Value must be at most 6.9.'}
    )
    rainfall = forms.FloatField(
        required=True,
        min_value=850,
        max_value=1200,
        error_messages={'required': 'Please enter a value for Rainfall.', 'min_value': 'Value must be at least 850.', 'max_value': 'Value must be at most 1200.'}
    )
    temperature = forms.FloatField(
        required=True,
        min_value=20,
        max_value=35,
        error_messages={'required': 'Please enter a value for Temperature.', 'min_value': 'Value must be at least 20.', 'max_value': 'Value must be at most 35.'}
    )
    humidity = forms.FloatField(
        required=True,
        min_value=40,
        max_value=90,
        error_messages={'required': 'Please enter a value for Humidity.', 'min_value': 'Value must be at least 40.', 'max_value': 'Value must be at most 90.'}
    )

    class Meta:
        model = Soildata
        fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'temperature', 'humidity', 'soil_type']


# --- New Forms for User Registration and Profile Update ---

class UserRegistrationForm(UserCreationForm):
    """
    A custom user creation form to use in our registration view.
    """
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class ProfileForm(forms.ModelForm):
    """
    A form for updating the user's profile details.
    """
    class Meta:
        model = Profile
        fields = ['photo', 'bio']