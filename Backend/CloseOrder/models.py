from django.db import models
from Register.models import Account
from OpenOrder.helper import generateUUID


class CloseOrders(models.Model):
    id = models.CharField(default=generateUUID, primary_key=True,
                          max_length=36, unique=True, editable=False)
    Chart_Symbol = models.CharField(max_length=32)
    Buy_price = models.FloatField()
    ClosePrice=models.FloatField(null=True)
    # Curr_price=models.IntegerField()
    Quantity = models.IntegerField()
    Profit=models.FloatField(null=True)
    Order_Number=models.FloatField(null=False)
    Exit_at = models.FloatField(null=True)
    Comment = models.CharField(max_length=32, null=True)
    Execution_Time = models.CharField(max_length=32, null=True)
    # Status=models.CharField(max_length=32)

    User = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "Close_Orders"
