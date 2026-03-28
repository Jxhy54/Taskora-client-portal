from django.contrib import admin
from .models import Request, Message


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'sender', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'sender__username', 'request__title')