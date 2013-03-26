import logging

log = logging.getLogger('tracking.listeners')

try:
    import traceback

    from django.core.cache import cache
    from django.db.models.signals import post_save, post_delete
    from django.db.utils import DatabaseError

    from tracking import utils
    from tracking.models import UntrackedUserAgent, BannedIP, Visitor, SiteObject
    from tracking.signals import site_object_requested
except ImportError:
    pass
else:

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

    def track_site_object(sender, **kwargs):
        """Saves information about site object requested by visitor"""
        request = kwargs['request']
        session_key = utils.get_session_key(request)
        ip_address = utils.get_ip(request)
        try:
            visitor = Visitor.objects.get(session_key=session_key, ip_address=ip_address)
        except Visitor.DoesNotExist:
            # track site object only if visitor is tracked
            return
        if not SiteObject.objects.filter(visitor=visitor).exists():
            site_object = SiteObject(content_object=sender, visitor=visitor)
            try:
                site_object.save()
            except DatabaseError:
                log.error('There was a problem saving site object information:\n%s\n\n%s' %
                          (traceback.format_exc(), locals()))


    post_save.connect(refresh_untracked_user_agents, sender=UntrackedUserAgent)
    post_delete.connect(refresh_untracked_user_agents, sender=UntrackedUserAgent)

    post_save.connect(refresh_banned_ips, sender=BannedIP)
    post_delete.connect(refresh_banned_ips, sender=BannedIP)

    site_object_requested.connect(track_site_object)
