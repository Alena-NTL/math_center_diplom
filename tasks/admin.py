from django.contrib import admin
from .models import Subject, Topic, DifficultyLevel, Task, TaskImage


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')
    list_editable = ('sort_order',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'grade', 'parent', 'sort_order')
    list_filter = ('subject', 'grade')
    list_editable = ('sort_order',)


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'numeric_value')


class TaskImageInline(admin.TabularInline):
    model = TaskImage
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_body', 'topic', 'difficulty', 'author', 'status', 'created_at')
    list_filter = ('status', 'difficulty', 'topic__subject', 'topic__grade')
    search_fields = ('body', 'answer')
    list_editable = ('status',)
    inlines = [TaskImageInline]

    def short_body(self, obj):
        return obj.body[:80] + '...' if len(obj.body) > 80 else obj.body
    short_body.short_description = 'Текст'
