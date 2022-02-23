from django.db import models
from Register.models import Account
from .helper import generateUUID


class OpenOrders(models.Model):
    id = models.CharField(default=generateUUID, primary_key=True,
                          max_length=36, unique=True, editable=False)
    Chart_Symbol = models.CharField(max_length=32)
    Buy_price = models.FloatField()
    # Curr_price=models.IntegerField()
    Quantity = models.IntegerField()
    # Profit=models.IntegerField()
    
    Terminal_Symbol=models.CharField(max_length=32,null=True)
    Token_id=models.CharField(max_length=32,null=True)
    Order_Number=models.IntegerField(null=False)
    Exit_at = models.FloatField(null=True)
    Status = models.CharField(max_length=32, null=True)
    Execution_Time = models.CharField(max_length=32, null=True)
    order_placed_time=models.DateTimeField(auto_now_add=True, blank=True)
    profit=models.FloatField(null=True)
    Exchange=models.CharField(max_length=32)
    # Status=models.CharField(max_length=32)

    User = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "Open_Orders"
