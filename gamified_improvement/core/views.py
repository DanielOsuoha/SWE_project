from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Plan, UserPlan
from .forms import UserProfileForm

@login_required
def index(request):
    # Define available categories
    categories = [
        {'slug': 'fitness', 'name': 'Fitness', 'icon': '💪'},
        {'slug': 'health', 'name': 'Health', 'icon': '🏥'},
        {'slug': 'education', 'name': 'Education', 'icon': '📚'},
        {'slug': 'career', 'name': 'Career', 'icon': '💼'},
        {'slug': 'mindfulness', 'name': 'Mindfulness', 'icon': '🧘'},
        {'slug': 'productivity', 'name': 'Productivity', 'icon': '⚡'},
    ]
    
    view_type = request.GET.get('view', 'discover')
    active_category = request.GET.get('category')
    search_query = request.GET.get('search', '')

    # Base queryset
    plans = Plan.objects.all()
    
    # Apply category filter if selected
    if active_category and active_category != 'all':
        plans = plans.filter(category=active_category)

    # Apply search filter if present
    if search_query:
        plans = plans.filter(title__icontains=search_query)

    # Split into my plans and discover plans
    my_plans = plans.filter(userplan__user=request.user)
    discover_plans = plans.exclude(userplan__user=request.user)

    context = {
        'categories': categories,
        'active_category': active_category,
        'view_type': view_type,
        'my_plans': my_plans,
        'discover_plans': discover_plans,
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