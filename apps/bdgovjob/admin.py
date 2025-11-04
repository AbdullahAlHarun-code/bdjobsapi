from django.contrib import admin
from .models import GovtJob


@admin.register(GovtJob)
class GovtJobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'vacancies', 'deadline', 'posted_date', 'created_at')
    list_filter = ('created_at', 'posted_date')
    search_fields = ('job_title', 'vacancies', 'deadline')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job_title', 'job_url', 'vacancies', 'deadline', 'posted_date')
        }),
        ('Metadata', {
            'fields': ('scraped_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

