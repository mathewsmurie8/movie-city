import csv
import json
from datetime import datetime
from django.contrib import admin
from .models import (
    Movie, RentalRate, RentalRequest)

class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'movie_type', 'genre', 'popularity', 'maximum_age',
        'created', 'updated', 'description', 'photo',)
    list_display_links = (
        'id', 'name', 'movie_type', 'genre', 'popularity',
        'maximum_age', 'photo')
    list_filter = ('movie_type', 'genre')
    search_fields = (
        'id', 'name', 'movie_type', 'genre', 'popularity', 'maximum_age',)
    list_per_page = 25

admin.site.register(Movie, MovieAdmin)


class RentalRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_type', 'daily_rate',)
    list_display_links = ('id', 'movie_type', 'daily_rate',)
    list_filter = ('id', 'movie_type', 'daily_rate',)
    search_fields = ('id', 'movie_type', 'daily_rate',)
    list_per_page = 25

admin.site.register(RentalRate, RentalRateAdmin)


class RentalRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'movie', 'start_date', 'end_date', 'total_amount',)
    list_display_links = (
        'id', 'movie', 'start_date', 'end_date', 'total_amount',)
    list_filter = (
        'id', 'movie', 'start_date', 'end_date', 'total_amount',)
    search_fields = (
        'id', 'movie__name', 'start_date', 'end_date', 'total_amount',)
    list_per_page = 25

admin.site.register(RentalRequest, RentalRequestAdmin)
