from django.contrib import admin

from serp_app import models


@admin.register(models.Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'cache_time_limit', 'default_user_agent')


@admin.register(models.Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('query', 'user_agent', 'timestamp', 'user_ip')


@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('search_id', 'header', 'link', 'position')
