from django.contrib import admin
from .models import Assignment, AssignmentTask, GeneratedPDF


class AssignmentTaskInline(admin.TabularInline):
    model = AssignmentTask
    extra = 0


class GeneratedPDFInline(admin.TabularInline):
    model = GeneratedPDF
    extra = 0
    readonly_fields = ('file', 'variant_number', 'generated_at')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'grade', 'created_at')
    inlines = [AssignmentTaskInline, GeneratedPDFInline]
