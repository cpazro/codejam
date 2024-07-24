

# Register your models here.
from django.contrib import admin
from .models import CommonSpace, \
                    Reservation, \
                    Category, \
                    Area


admin.site.register(CommonSpace)
admin.site.register(Reservation)
admin.site.register(Category)
admin.site.register(Area)
