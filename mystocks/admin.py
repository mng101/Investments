from django.contrib import admin

# Register your models here.

from mystocks.models import User

admin.site.register(User)
