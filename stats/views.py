from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Max, Avg


from .models import Gauge
from .models import GaugeValue
from .models import Event
from .models import EventValue

import datetime
from django.utils import timezone

import random

from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from graphos.renderers.gchart import LineChart

graph_options = [
            {'days': 1, 'resolution': 'minute'},
            {'days': 7, 'resolution': 'hour'},
            {'days': 30, 'resolution': 'hour'},
            {'days': 356, 'resolution': 'day'},
]

def stats(request):

    context = {'charts': []}

    for gauge in Gauge.objects.all():
        chart_last_day = gauge_chart(gauge, graph_options[0]['days'], graph_options[0]['resolution'])
        chart_last_week = gauge_chart(gauge, graph_options[1]['days'], graph_options[1]['resolution'])
        last_updated = GaugeValue.objects.filter(gauge=gauge).aggregate(Max('created_at'))['created_at__max']
        context['charts'].append({'chart_last_day': chart_last_day,
                                  'chart_last_week': chart_last_week,
                                   'title': gauge.title,
                                   'desc': gauge.desc,
                                   'slug': gauge.slug,
                                   'last_updated': last_updated
                                 })

    return render(request, 'stats.html', context)

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

def event_add(request, slug):
    value = request.GET.get('value') or None
    secret = request.GET.get('secret') or None

    try:
        event = Event.objects.get(slug = slug)
    except ObjectDoesNotExist as e:
        title = slug.replace("-", " ").title()
        event = Event(slug=slug, secret=secret, title=title)
        event.save()

    if event.secret and event.secret != secret:
        return HttpResponseBadRequest("Wrong secret")
    if not value:
        return HttpResponseBadRequest("No value found")

    event_value = EventValue(event=event, value=value)
    event_value.save()

    return HttpResponse()

def gauge_show(request, slug):
    context = {'charts': []}

    for gauge in Gauge.objects.filter(slug=slug):
        context['desc'] = gauge.desc
        context['title'] = gauge.title
        for option in graph_options:
            chart = gauge_chart(gauge, option['days'], option['resolution'])
            context['charts'].append(chart)

    return render(request, 'gauge.html', context)



##################
# Help functions #
##################

def gauge_chart(gauge, days, resolution):
    now = timezone.now()
    yesterday = now - timezone.timedelta(hours = 24*days)

    queryset = GaugeValue.objects.filter(gauge=gauge)\
                                 .filter(created_at__range=(yesterday, now))\
                                 .extra({resolution: "date_trunc('"+resolution+"', created_at)"})\
                                 .values(resolution).order_by().annotate(avg=Avg('value'))\
                                 .order_by(resolution).all()

    unit = gauge.unit if gauge.unit else "missing"
    a = [['Time', unit]]
    for row in queryset:
        a.append( [ row[resolution] , row['avg'] ])

    data_source = SimpleDataSource(data=a)
    title = "{} - {} dager ({:4.2f})".format(gauge.title,
                                       days,
                                       queryset.reverse()[0]['avg'])

    chart = LineChart(data_source, options={'title': title,
                                            'curveType': 'function',
                                           })
    return chart
