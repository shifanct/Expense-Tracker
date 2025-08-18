from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Monthly_budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_monthly_budget')
    budget = models.IntegerField()
    month = models.CharField(max_length=50)
    added_on = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'month')

    def __str__(self):
        return f'{self.user}\' {self.month} budget'