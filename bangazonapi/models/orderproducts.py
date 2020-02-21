from django.db import models
from .orders import Order
from .products import Product

class OrderProduct(models.model):
    """
        This represents a Order Product object

        foreign keys: customer, product_type

        Author: Michelle Johnson
    """

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ("-create_at",)
        verbose_name = ("order product")
        verbose_name_plural = ("order products")

    def __str__(self):
        return f'Order {self.order.id} has the following product \n ${self.product.name}' 