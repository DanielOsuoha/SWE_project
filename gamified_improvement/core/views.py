from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Plan, UserPlan
from .forms import UserProfileForm

@login_required
def index(request):
    # Get category filter
    category = request.GET.get('category')
    
    # Base querysets
    all_plans = Plan.objects.all()
    if category:
        all_plans = all_plans.filter(category=category)
        
    # Get user's plans
    my_plans = Plan.objects.filter(
        userplan__user=request.user
    ).order_by('-userplan__started_at')
    
    # Get plans to discover (excluding user's plans)
    discover_plans = all_plans.exclude(
        id__in=my_plans.values_list('id', flat=True)
    ).order_by('-rating')
    
    context = {
        'my_plans': my_plans,
        'discover_plans': discover_plans,
        'active_category': category,
        'streak': request.user.profile.streak if hasattr(request.user, 'profile') else 0
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
    
    # Check if user already has this plan
    user_plan, created = UserPlan.objects.get_or_create(
        user=request.user,
        plan=plan
    )
    
    if created:
        messages.success(request, f'You have successfully started "{plan.title}"!')
    else:
        messages.info(request, f'You are already working on "{plan.title}".')
    
    return redirect('core:index')