from django.contrib import admin

from core.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['title', 'content']
    date_hierarchy = 'created'
