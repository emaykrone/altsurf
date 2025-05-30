from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'pixel_id', 'created_at')
    search_fields = ('name', 'domain', 'pixel_id')
    readonly_fields = ('pixel_id', 'created_at') # pixel_id генерируется автоматически