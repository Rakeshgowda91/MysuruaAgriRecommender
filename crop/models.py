# crop/models.py
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Soildata(models.Model):
    # These fields correspond to the input data for the ML model
    nitrogen = models.FloatField(default=0.0)
    phosphorus = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    ph = models.FloatField(default=0.0)
    rainfall = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    soil_type = models.CharField(max_length=50, default='Red')
    
    # This field will store the recommended crop after prediction
    crop_result = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Soil Data: N={self.nitrogen}, P={self.phosphorus}, K={self.potassium}, pH={self.ph}"

class Article(models.Model):
    title = models.CharField(max_length=200)
    
    # Use RichTextUploadingField to enable file and image uploads in the editor
    content = RichTextUploadingField()
    
    # Optional field for a thumbnail image
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)
    
    # Automatically records the date and time of creation
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# --- New Models for User Profile ---

class Profile(models.Model):
    # Link the profile to a Django User instance (one-to-one relationship)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Field for the profile photo
    photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.png', blank=True)
    
    # Optional: Add more fields if you need them (e.g., bio, location)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

# --- Signals to automatically create/update Profile when a User is created/updated ---

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()