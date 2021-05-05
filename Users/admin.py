# coding=utf-8
from django.contrib import admin
from .models import CD


class CDAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "artist", "genre")
    empty_value_display = "-пусто-"
    list_filter = ("date", "genre")


admin.site.register(CD, CDAdmin)
