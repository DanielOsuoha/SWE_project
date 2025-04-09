from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'rating')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description')
    ordering = ('-rating', 'title')