from .customers import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from django.db import models
from creditcards.models import CardExpiryField


class PaymentType(SafeDeleteModel):
    '''
    This class creates the model for payment types
    Author: Lauren Riddle
    '''
    _safedelete_policy = SOFT_DELETE

    merchant_name = models.CharField(max_length=25)
    account_number = models.CharField(max_length=25)
    expiration_date = CardExpiryField(('expiration date'))
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("payment type")
        verbose_name_plural = ("payment types")

    def __str__(self):
        return f'Your {self.merchant_name} card number is {self.account_number}'