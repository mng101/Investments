from django.contrib import admin
from stocks.models import User, Stock, Portfolio

# Register your models here.

admin.site.register(User)
admin.site.register(Stock)
admin.site.register(Portfolio)