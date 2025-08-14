from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_income')
    date = models.DateField()
    amount = models.IntegerField()

    SOURCE_CHOICES = [
        ('salary', 'Salary'),
        ('freelance', 'Freelance'),
        ('gift', 'Gift'),
        ('investment', 'Investment'),
    ]
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.source} on {self.date}'


