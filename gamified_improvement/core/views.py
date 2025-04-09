from django.shortcuts import render

def home(request):
    return render(request, 'core/index.html')

def leaderboard(request):
    return render(request, 'core/leaderboard.html')

def friends(request):
    return render(request, 'core/friends.html')

def profile(request):
    return render(request, 'core/profile.html')