from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Plan
from .forms import UserProfileForm

@login_required
def index(request):
    categories = [
        {'name': 'All', 'slug': 'all', 'icon': '🎯'},
        {'name': 'Fitness', 'slug': 'fitness', 'icon': '💪'},
        {'name': 'Health', 'slug': 'health', 'icon': '❤️'},
        {'name': 'Personal', 'slug': 'personal', 'icon': '🎯'},
        {'name': 'Career', 'slug': 'career', 'icon': '💼'},
        {'name': 'Financial', 'slug': 'financial', 'icon': '💰'},
    ]
    
    active_category = request.GET.get('category', 'all')
    view_type = request.GET.get('view', 'discover')  # Default to discover view
    

    all_plans = Plan.objects.all()
    my_plans = Plan.objects.filter(userplan__user=request.user, userplan__is_active=True)
    
    discover_plans = all_plans.exclude(id__in=my_plans.values_list('id', flat=True))
    
    # Apply category filter if needed
    if active_category and active_category != 'all':
        my_plans = my_plans.filter(category=active_category)
        discover_plans = discover_plans.filter(category=active_category)
    
    # Order plans
    my_plans = my_plans.order_by('-rating', 'title')
    discover_plans = discover_plans.order_by('-rating', 'title')
    
    context = {
        'categories': categories,
        'my_plans': my_plans,
        'discover_plans': discover_plans,
        'active_category': active_category,
        'view_type': view_type,
        'streak': request.user.profile.streak if hasattr(request.user, 'profile') else 0,
    }
    return render(request, 'core/index.html', context)


def leaderboard(request):
    return render(request, 'core/leaderboard.html')

def friends(request):
    return render(request, 'core/friends.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'streak': request.user.profile.streak if hasattr(request.user, 'profile') else 0
    }
    return render(request, 'core/profile.html', context)

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
def plan_detail(request, pk):
    """
    Display detailed information about a specific plan.
    Args:
        request: The HTTP request
        pk: The primary key of the Plan
    """
    plan = get_object_or_404(Plan, pk=pk)
    
    context = {
        'plan': plan,
        'streak': request.user.profile.streak if hasattr(request.user, 'profile') else 0,
    }
    return render(request, 'core/plans/detail.html', context)


def save_change(request):
    """
    Save changes made to the user's profile.
    Args:
        request: The HTTP request
    """
    if request.method == 'POST':
        if form.is_valid():
            
            messages.success(request, 'Your profile was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    return redirect('core:profile')

@login_required
def start_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    # Add logic here to start the plan for the user
    plan.my_plan = True
    plan.save()
    messages.success(request, f'You have successfully started "{plan.title}"!')
    return redirect('core:plan_detail', pk=pk)