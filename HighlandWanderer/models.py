from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Category model for dynamic location categories.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    views = models.PositiveIntegerField(default=0)  # Record the number of views

    def __str__(self):
        return self.name

# Profile model to extend the built-in User model with an avatar.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to automatically create a Profile when a new User is created.
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Location model to store hiking location details.
class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    # Use ForeignKey to Category instead of hard-coded choices.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='locations')
    beautiful = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comfortable = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    traffic = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    image1 = models.ImageField(upload_to='locations/', blank=True, null=True)
    image2 = models.ImageField(upload_to='locations/', blank=True, null=True)

    def __str__(self):
        return self.name

# Comment model for location comments.
class Comment(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.location.name}'

