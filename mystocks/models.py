from django.db import models
from django.urls import reverse

# Create your models here.

# If you’re starting a new project, it’s highly recommended to set up a custom user model, even
# if the default User model is sufficient for you. This model behaves identically to the default
# user model, but you’ll be able to customize it in the future if the need arises:
#
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Stock(models.Model):
    """Model representing the list of Stocks to be tracked"""
    symbol = models.CharField(max_length=12, unique=True, )
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    # dividend = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    # exdivdate = models.DateField(null=True, blank=True)
    # CURRENCIES = (
    #     ('C', 'CAD'),
    #     ('U', 'US$'),
    # )
    # currency = models.CharField(max_length=1, choices=CURRENCIES)
    # FREQUENCIES = (
    #     ('M', 'Monthly'),
    #     ('Q', 'Quarterly'),
    #     ('S', 'Semi Annual'),
    #     ('A', 'Annual'),
    #     ('N', 'No Div'),
    # )
    # frequency = models.CharField(max_length=1, choices=FREQUENCIES)

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    def get_absolute_url(self):
        """Returns the URL to access a particular Symbol details"""
        return reverse("detail", kwargs={'pk':self.pk})

    def clean(self):
        self.symbol = self.symbol.upper()
