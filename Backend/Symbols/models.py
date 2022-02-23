from django.db import models
from Register.models import Account

Market_Choice = (
    ("1", "NSE"),
    ("2", "BSE"),
    ("3", "MCX") ,
    ("4","NFO")
)


class Symbols(models.Model):
    Market = models.CharField(max_length=1, choices=Market_Choice)
    Chart_Symbol = models.CharField(max_length=32)
    Token_id=models.CharField(max_length=32,null=True)
    Terminal_Symbol = models.CharField(max_length=32)
    Stoploss = models.FloatField()
    Limit = models.FloatField()
    Quantity = models.IntegerField()
    User = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "Symbols"
