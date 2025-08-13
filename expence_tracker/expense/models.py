from django.db import models

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
