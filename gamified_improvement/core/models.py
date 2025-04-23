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
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'plan')

    def create_user_goals(self):
        """Create UserGoal instances for each Goal in the plan"""
        for goal in self.plan.goals.all():
            UserGoal.objects.get_or_create(
                user_plan=self,
                goal=goal
            )

    def update_progress(self):
        """Update progress based on completed goals"""
        total_goals = self.user_goals.count()
        if total_goals > 0:
            completed_goals = self.user_goals.filter(completed=True).count()
            self.progress = int((completed_goals / total_goals) * 100)
            self.save()

class Goal(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class UserGoal(models.Model):
    user_plan = models.ForeignKey(UserPlan, on_delete=models.CASCADE, related_name='user_goals')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user_plan', 'goal')

    def __str__(self):
        return f"{self.goal.title} - {self.user_plan.user.username}"
