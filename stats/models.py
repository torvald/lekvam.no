from django.db import models
from django.contrib.auth.models import User


class Gauge(models.Model):
    slug = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    secret = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    deleted = models.DateTimeField(null=True, blank=True)

    @property
    def avg(self):
        # TODO
        return ""

    def __str__(self):
        return self.title


class GaugeValue(models.Model):
    gauge = models.ForeignKey(Gauge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return str(self.gauge) + ": " + str(self.value)

