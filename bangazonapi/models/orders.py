from django.db import models
from .customers import Customer
from .paymenttypes import PaymentType

class Order(models.Model):
    """
    This class is responsible for creating the order instances.

    Author: 
        Ryan Crowley
    """

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = ("order")
        verbose_name_plural = ("orders")

    def __str__(self):
        return f'''
        Order: {self.id} 
        Customer: {self.customer.user.first_name} {self.customer.user.last_name}
        '''

    


