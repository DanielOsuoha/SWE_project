from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    CATEGORY_CHOICES = [
        ('fitness', '💪 Fitness'),
        ('health', '❤️ Health'),
        ('personal', '🎯 Personal'),
        ('career', '💼 Career'),
        ('financial', '💰 Financial'),
        ('spiritual', '🧘 Spiritual'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🎯')
    rating = models.IntegerField(default=5)
    users = models.ManyToManyField(User, through='UserPlan', related_name='plans')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', 'title']

    def __str__(self):
        return self.title

    def get_icon(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, '🎯').split()[0]

class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'plan')
