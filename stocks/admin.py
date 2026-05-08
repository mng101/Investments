from django.contrib import admin
from stocks.models import User, Stock, Portfolio, Holding

# Register your models here.

admin.site.register(User)
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Holding)