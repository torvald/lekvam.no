from django.contrib import admin

# Register your models here.
from .models import Gauge, GaugeValue

admin.site.register(GaugeValue)
admin.site.register(Gauge)
