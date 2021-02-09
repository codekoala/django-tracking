from django.contrib import admin
from tracking.models import Visitor, VisitorManager, BannedIP, UntrackedUserAgent

class VisitorAdmin(admin.ModelAdmin):
    search_fields = ['username']
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(BannedIP)
admin.site.register(UntrackedUserAgent)
