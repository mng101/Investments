from django.contrib import admin
from stocks.models import User, Stock

# Register your models here.

admin.site.register(User)
admin.site.register(Stock)