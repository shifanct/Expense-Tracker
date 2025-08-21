from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DailyExpense(models.Model):
    date = models.DateField()
    expense_type_choices = [('transport','Transportation'),
                            ('food','Food & Diningd'),
                            ('rent','Rent'),
                            ('medical','Medical'),
                            ('utilities','Utilities'),
                            ('clothing','Clothing'),
                            ('entertainment','Entertaininment'),
                            ('vehcles','Vehcles'),
                            ]
    expense_type = models.CharField(choices=expense_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_expense', null=True, blank=True)
    def model_name(self):
        return self._meta.model_name

    def __str__(self):
        return f'{self.expense_type} on {self.date}'