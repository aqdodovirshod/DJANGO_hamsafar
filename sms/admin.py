from django.contrib import admin
from .models import Trip, Request

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_location', 'end_location', 'date', 'seats')
    list_filter = ('date', 'user')
    search_fields = ('start_location', 'end_location', 'user__username')
    date_hierarchy = 'date'

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_location', 'end_location', 'date')
    list_filter = ('date', 'user')
    search_fields = ('start_location', 'end_location', 'user__username')
    date_hierarchy = 'date'
