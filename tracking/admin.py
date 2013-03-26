from django.contrib import admin
from tracking.models import BannedIP, UntrackedUserAgent, Visitor, SearchItem, SiteObject

def visitor_session(obj):
    return obj.visitor.session_key

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'ip_address', 'user_agent', 'referrer',
                    'url', 'page_views', 'session_start', 'last_update')

class SearchItemAdmin(admin.ModelAdmin):
    list_display = ('engine', 'query', visitor_session)

class SiteObjectAdmin(admin.ModelAdmin):
    list_display = ('content_object', visitor_session)

admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(SearchItem, SearchItemAdmin)
admin.site.register(SiteObject, SiteObjectAdmin)
