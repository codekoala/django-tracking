from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from past.utils import old_div
from datetime import datetime, timedelta
import logging
import traceback

from django.contrib.gis.geoip import GeoIP, GeoIPException
try:
    from django.conf import settings
    User = settings.AUTH_USER_MODEL
except AttributeError:
    from django.conf import settings
    from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from tracking import utils

USE_GEOIP = getattr(settings, 'TRACKING_USE_GEOIP', False)
CACHE_TYPE = getattr(settings, 'GEOIP_CACHE_TYPE', 4)

log = logging.getLogger('tracking.models')

class VisitorManager(models.Manager):
    def active(self, timeout=None):
        """
        Retrieves only visitors who have been active within the timeout
        period.
        """
        if not timeout:
            timeout = utils.get_timeout()

        now = utils.get_now()
        cutoff = now - timedelta(minutes=timeout)

        return self.get_queryset().filter(last_update__gte=cutoff)

class Visitor(models.Model):
    session_key = models.CharField(max_length=40)
    ip_address = models.CharField(max_length=20)
    user = models.ForeignKey(User, null=True)
    user_agent = models.CharField(max_length=255)
    referrer = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    page_views = models.PositiveIntegerField(default=0)
    session_start = models.DateTimeField()
    last_update = models.DateTimeField()

    objects = VisitorManager()

    def _time_on_site(self):
        """
        Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database.
        """
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = old_div(seconds, 3600)
            seconds -= hours * 3600
            minutes = old_div(seconds, 60)
            seconds -= minutes * 60

            return u'%i:%02i:%02i' % (hours, minutes, seconds)
        else:
            return ugettext(u'unknown')
    time_on_site = property(_time_on_site)

    def _get_geoip_data(self):
        """
        Attempts to retrieve MaxMind GeoIP data based upon the visitor's IP
        """

        if not HAS_GEOIP or not USE_GEOIP:
            # go no further when we don't need to
            log.debug('Bailing out.  HAS_GEOIP: %s; TRACKING_USE_GEOIP: %s' % (HAS_GEOIP, USE_GEOIP))
            return None

        if not hasattr(self, '_geoip_data'):
            self._geoip_data = None
            try:
                gip = GeoIP(cache=CACHE_TYPE)
                self._geoip_data = gip.city(self.ip_address)
            except GeoIPException:
                # don't even bother...
                log.error('Error getting GeoIP data for IP "%s": %s' % (self.ip_address, traceback.format_exc()))

        return self._geoip_data

    geoip_data = property(_get_geoip_data)

    def _get_geoip_data_json(self):
        """
        Cleans out any dirty unicode characters to make the geoip data safe for
        JSON encoding.
        """
        clean = {}
        if not self.geoip_data: return {}

        for key,value in list(self.geoip_data.items()):
            clean[key] = utils.u_clean(value)
        return clean

    geoip_data_json = property(_get_geoip_data_json)

    class Meta(object):
        ordering = ('-last_update',)
        unique_together = ('session_key', 'ip_address',)

class UntrackedUserAgent(models.Model):
    keyword = models.CharField(_('keyword'), max_length=100, help_text=_('Part or all of a user-agent string.  For example, "Googlebot" here will be found in "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" and that visitor will not be tracked.'))

    def __unicode__(self):
        return self.keyword

    class Meta(object):
        ordering = ('keyword',)
        verbose_name = _('Untracked User-Agent')
        verbose_name_plural = _('Untracked User-Agents')

class BannedIP(models.Model):
    ip_address = models.GenericIPAddressField('IP Address', help_text=_('The IP address that should be banned'))

    def __unicode__(self):
        return self.ip_address

    class Meta(object):
        ordering = ('ip_address',)
        verbose_name = _('Banned IP')
        verbose_name_plural = _('Banned IPs')


# Listners
def refresh_untracked_user_agents(sender, instance, created=False, **kwargs):
    """Updates the cache of user agents that we don't track"""

    log.debug('Updating untracked user agents cache')
    cache.set('_tracking_untracked_uas',
        UntrackedUserAgent.objects.all(),
        3600)

def refresh_banned_ips(sender, instance, created=False, **kwargs):
    """Updates the cache of banned IP addresses"""

    log.debug('Updating banned IP cache')
    cache.set('_tracking_banned_ips',
        [b.ip_address for b in BannedIP.objects.all()],
        3600)

post_save.connect(refresh_untracked_user_agents, sender=UntrackedUserAgent)
post_delete.connect(refresh_untracked_user_agents, sender=UntrackedUserAgent)

post_save.connect(refresh_banned_ips, sender=BannedIP)
post_delete.connect(refresh_banned_ips, sender=BannedIP)
