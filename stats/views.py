from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Max

from .models import Gauge
from .models import GaugeValue

import datetime
import random

def stats(request):
    pass

def gauge_add(request, slug):
    value = request.GET.get('value') or None
    secret = request.GET.get('secret') or None

    try:
        gauge = Gauge.objects.get(slug = slug)
    except ObjectDoesNotExist as e:
        title = slug.replace("-", " ").title()
        gauge = Gauge(slug=slug, secret=secret, title=title)
        gauge.save()

    if gauge.secret and gauge.secret != secret:
        return HttpResponseBadRequest("Wrong secret")
    if not value:
        return HttpResponseBadRequest("No value found")

    gauge_value = GaugeValue(gauge=gauge, value=value)
    gauge_value.save()

    return HttpResponse()
