from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'status', 'tickets_sold', 'capacity')
    list_filter = ('status', 'date')
    search_fields = ('name', 'details')
