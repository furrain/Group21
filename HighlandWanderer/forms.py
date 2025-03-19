from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Category, Location


# Registration form for new users.
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Profile form for updating user profile.
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()
                profile.save()
        return profile


# Comment form for adding comments to a location.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }


# Form for adding a new Category (admin functionality).
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


# Form for adding a new Location (admin functionality).
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'address', 'category', 'beautiful', 'comfortable', 'traffic', 'image1', 'image2']