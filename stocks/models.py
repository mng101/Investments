from django.db import models
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import date

# Create your models here.

# If you’re starting a new project, it’s highly recommended to set up a custom user model, even
# if the default User model is sufficient for you. This model behaves identically to the default
# user model, but you’ll be able to customize it in the future if the need arises:
#
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Stock(models.Model):
    """
    Model to capture some details of Stocks to be tracked
    """

    FREQUENCIES = ( # dividend frequency
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('S', 'Semi-Annual'),
        ('A', 'Annually'),
    )

    CURRENCIES = ( # Currency in which dividend is paid. Some securites that trade in CAD pay dividend in USD
        ('C', 'CAD'),
        ('U', 'USD'),
    )

    symbol = models.CharField(max_length=12, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    notes = models.CharField(max_length=1024, blank=True)
    ex_div_date = models.DateField(default=date.today)
    dividend = models.DecimalField(max_digits=6, decimal_places=4, default=0.0000)
    frequency = models.CharField(max_length=1, choices=FREQUENCIES, default='Q')
    currency = models.CharField(max_length=1, choices=CURRENCIES, default='C')

    last_baystreet_entry = models.DateField(default="2025-07-01")
    last_analyst_rating = models.DateField(default="2025-07-01")

    # Image fields populated by the PIL "grabimage" functions
    # These fields are not included in the StockForm, since the default handling of an Image Field
    # uploaded from a file, is not suitable for the desired user interaction
    #
    # ***** NOTE *****
    #
    # Analyst Ratings do not apply to some securities such as Preferred Shares, Units, etc.
    # For these securities, recommendation is to manually update the Bay Street and Anlayst
    # Rating update dates to 2030-12-31 through the Admin interface so that these securities
    # can be filtered out in selected views

    img1 = models.ImageField( # Bay Street Analyst price targets BMOIL site
        upload_to='stocks/',
        default='stocks/Default1.png',
        null="True", blank="True"
    )
    last_update_1 = models.DateTimeField(auto_now_add=True)
    img1_refreshed_on = models.DateField(default='2025-01-01')
    # img1_last_analyst_entry = models.DateField(default="2025-01-01")

    img2 = models.ImageField( # Analyst price target on Webbroker site
        upload_to='stocks/',
        default='stocks/Default2.png',
        null="True", blank="True"
    )
    last_update_2 = models.DateTimeField(auto_now_add="True")
    img2_refreshed_on = models.DateField(default='2025-01-01')
    # img2_last_analyst_entry = models.DateField(default="2025-01-01")

    class Meta:
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    def get_absolute_url(self):
        """ Displays the values submitted following the DB update """
        return reverse("update", kwargs={'pk': self.pk})

    def clean(self):
        """ Ensure the Symbol is converted to Uppercase before saving the record """
        self.symbol = self.symbol.upper()

    def save(self, *args, **kwargs):
        print("In Stock Save")
        # current = Stock.objects.get(symbol=self.symbol)

        try:
            this = Stock.objects.get(symbol=self.symbol)
        except ObjectDoesNotExist:
            pass

        super(Stock, self).save(*args, **kwargs)
