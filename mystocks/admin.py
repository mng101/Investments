from django.contrib import admin

# Register your models here.

from mystocks.models import User, Stock

admin.site.register(User)
admin.site.register(Stock)
