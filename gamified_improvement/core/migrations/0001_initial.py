# Generated by Django 5.2 on 2025-04-09 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('fitness', '💪 Fitness'), ('health', '❤️ Health'), ('personal', '🎯 Personal'), ('career', '💼 Career'), ('financial', '💰 Financial'), ('spiritual', '🧘 Spiritual')], max_length=50)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('description', models.TextField()),
                ('icon', models.CharField(default='🎯', max_length=10)),
                ('rating', models.IntegerField(default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-rating', 'title'],
            },
        ),
    ]
