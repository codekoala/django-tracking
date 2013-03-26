import django.dispatch
import logging

log = logging.getLogger('tracking.signals')


site_object_requested = django.dispatch.Signal(providing_args=["request"])
