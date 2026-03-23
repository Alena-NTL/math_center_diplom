from django.contrib import admin
from .models import ModerationLog


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'moderator', 'action', 'created_at')
    list_filter = ('action',)
    readonly_fields = ('task', 'moderator', 'action', 'comment', 'created_at')
