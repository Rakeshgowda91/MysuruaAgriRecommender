# crop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import os
import joblib
import pandas as pd
import numpy as np
from .models import Article, Soildata, Profile
from .forms import SoilDataForm, UserRegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# --- ML Model Loading ---
model_path = os.path.join(settings.BASE_DIR, 'crop_model.pkl')
soil_encoder_path = os.path.join(settings.BASE_DIR, 'soil_encoder.pkl')
crop_encoder_path = os.path.join(settings.BASE_DIR, 'crop_encoder.pkl')

model = None
soil_encoder = None
crop_encoder = None

try:
    if os.path.exists(model_path) and os.path.exists(soil_encoder_path) and os.path.exists(crop_encoder_path):
        model = joblib.load(model_path)
        soil_encoder = joblib.load(soil_encoder_path)
        crop_encoder = joblib.load(crop_encoder_path)
        print("✅ ML model and encoders loaded successfully!")
    else:
        print("WARNING: One or more ML model files (.pkl) not found at expected paths. Crop recommendation will not work.")
except Exception as e:
    print(f"Error loading ML model files: {e}. Crop recommendation will not work.")
    model = None
    soil_encoder = None
    crop_encoder = None

# --- Helper Function for ML Prediction ---
def get_recommended_crop(n, p, k, ph, rainfall, temperature, humidity, soil_type_str):
    """
    Predicts the recommended crop using the loaded ML model and encoders.
    Returns the decoded crop name or an error message.
    """
    if not model or not soil_encoder or not crop_encoder:
        return "Model or encoders not available."

    try:
        encoded_soil_type = soil_encoder.transform([soil_type_str])[0]
        
        input_data = pd.DataFrame([[n, p, k, ph, rainfall, temperature, humidity, encoded_soil_type]],
                                  columns=['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'temperature', 'humidity', 'soil_type'])
        
        prediction_encoded = model.predict(input_data)[0]
        
        recommended_crop_name = crop_encoder.inverse_transform([prediction_encoded])[0]
        
        return recommended_crop_name
    except Exception as e:
        print(f"Error during ML prediction: {e}")
        return "Prediction failed due to an internal error."

# --- Main View for Crop Recommendation ---
def index(request):
    """
    This view serves as the main homepage. It now redirects to the login page
    if the user is not authenticated.
    """
    # Check if the user is logged in. If not, redirect to the login page.
    if not request.user.is_authenticated:
        return redirect('login') # 'login' is the name of the URL pattern for the login page

    # If the user is authenticated, proceed with the normal view logic
    form = SoilDataForm()
    recommended_crop_result = None

    if request.method == 'POST':
        form = SoilDataForm(request.POST)
        if form.is_valid():
            soil_data_instance = form.save(commit=False)
            
            recommended_crop_result = get_recommended_crop(
                soil_data_instance.nitrogen,
                soil_data_instance.phosphorus,
                soil_data_instance.potassium,
                soil_data_instance.ph,
                soil_data_instance.rainfall,
                soil_data_instance.temperature,
                soil_data_instance.humidity,
                soil_data_instance.soil_type
            )
            
            soil_data_instance.crop_result = recommended_crop_result
            soil_data_instance.save()
        else:
            recommended_crop_result = "Please fill out all the fields with valid data."

    articles = Article.objects.order_by('-posted_at')[:3]
    
    context = {
        'form': form,
        'result': recommended_crop_result,
        'articles': articles
    }
    return render(request, 'crop/index.html', context)

# --- Other Views ---

def article_list(request):
    """
    View to display a list of all published articles.
    """
    articles = Article.objects.order_by('-posted_at')
    return render(request, 'crop/article_list.html', {'articles': articles})

def article_detail(request, pk):
    """
    View to display a single article in detail.
    """
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'crop/article_detail.html', {'article': article})

# --- Views for User Authentication ---

def register(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('profile')
    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def profile(request):
    """
    Displays and handles updates for the user's profile and photo.
    """
    profile_instance, created = Profile.objects.get_or_404(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile') 
    else:
        profile_form = ProfileForm(instance=profile_instance)

    context = {
        'profile_form': profile_form,
        'profile': profile_instance
    }
    return render(request, 'crop/profile.html', context)