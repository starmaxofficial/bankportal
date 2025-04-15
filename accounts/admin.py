from django.contrib import admin
from .models import Statement

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'uploaded_at')
    search_fields = ('title', 'user__username')
    list_filter = ('uploaded_at',)
