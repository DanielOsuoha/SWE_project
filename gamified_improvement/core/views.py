from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Plan

@login_required
def index(request):
    # Predefined categories with icons
    categories = [
        {'name': 'All', 'slug': 'all', 'icon': '🎯'},
        {'name': 'Fitness', 'slug': 'fitness', 'icon': '💪'},
        {'name': 'Health', 'slug': 'health', 'icon': '❤️'},
        {'name': 'Personal', 'slug': 'personal', 'icon': '🎯'},
        {'name': 'Career', 'slug': 'career', 'icon': '💼'},
        {'name': 'Financial', 'slug': 'financial', 'icon': '💰'},
    ]
    
    # Get all plans, ordered by rating
    plans = Plan.objects.all().order_by('-rating', 'title')
    
    context = {
        'categories': categories,
        'plans': plans,
        'streak': request.user.profile.streak if hasattr(request.user, 'profile') else 0,
    }
    return render(request, 'core/index.html', context)

def home(request):
    return render(request, 'core/index.html')

def leaderboard(request):
    return render(request, 'core/leaderboard.html')

def friends(request):
    return render(request, 'core/friends.html')

def profile(request):
    return render(request, 'core/profile.html')

def about(request):
    return render(request, 'core/about.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('core:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'core/change_password.html', {
        'form': form
    })

@login_required
def plan_list(request):
    plans = Plan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, 'core/plans/list.html', context)

@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    context = {
        'plan': plan,
    }
    return render(request, 'core/plans/detail.html', context)