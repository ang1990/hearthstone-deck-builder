# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import HearthstoneCard

from django.contrib import admin


# Register your models here.

class HearthstoneCardAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'cardId',
        'dbfId',
        'name',
        'cardSet',
        'type',
        'text',
        'playerClass',
        'locale'
    ]


admin.site.register(HearthstoneCard, HearthstoneCardAdmin)
