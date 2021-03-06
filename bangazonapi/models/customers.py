from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
    """
    This makes a customer instance
    Author:
    Trey Suiter
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=7, null=True)
    phone = models.CharField(max_length=14, null=True)

    class Meta:
        verbose_name = ("customer")
        verbose_name_plural = ("customers")
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
        
#!This is not needed due to using ORM
# These receiver hooks allow you to continue to
# work with the `User` class in your Python code.
# Every time a `User` is created, a matching `Customer`
# object will be created and attached as a one-to-one
# property
# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
# # Every time a `User` is saved, its matching `Customer`
# # object will be saved.
# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()  