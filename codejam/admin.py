

# Register your models here.
from django.contrib import admin
from .models import CommonSpace, Reservation

admin.site.register(CommonSpace)
admin.site.register(Reservation)
