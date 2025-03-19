from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Location, Comment, Category
from .forms import RegistrationForm, ProfileForm, CommentForm, CategoryForm, LocationForm
from django.db.models import Q
from django.http import JsonResponse



def home(request):
    categories = Category.objects.all()  # Load all categories dynamically.
    return render(request, 'HighlandWanderer/home.html', {'categories': categories})

def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    # Update views
    category.views += 1
    category.save()
    locations = Location.objects.filter(category=category)
    return render(request, 'HighlandWanderer/category.html', {'locations': locations, 'category': category})


def search_results(request):
    query = request.GET.get('q', '')
    order = request.GET.get('order', '')
    locations = Location.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query)
    )
    if order in ['beautiful', 'comfortable', 'traffic']:
        locations = locations.order_by('-' + order)
    else:
        locations = locations.order_by('-created_at')
    return render(request, 'HighlandWanderer/search_results.html', {'locations': locations, 'query': query})

def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    comments = location.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.location = location
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully.')
                return redirect('location_detail', location_id=location.id)
        else:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
    else:
        form = CommentForm()
    return render(request, 'HighlandWanderer/location_detail.html', {
        'location': location,
        'comments': comments,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'HighlandWanderer/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile, user=request.user)
    return render(request, 'HighlandWanderer/profile.html', {'form': form})

# New admin view: Add Category
@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'HighlandWanderer/add_category.html', {'form': form})

# New admin view: Add Location
@staff_member_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location added successfully.')
            return redirect('home')
    else:
        form = LocationForm()
    return render(request, 'HighlandWanderer/add_location.html', {'form': form})


def about_us(request):
    return render(request, 'HighlandWanderer/about_us.html')

