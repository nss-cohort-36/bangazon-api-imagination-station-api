from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):

    """
    This makes a customer instance

    Author:
    Trey Suiter
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("customer")
        verbose_name_plural = ("customers")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

