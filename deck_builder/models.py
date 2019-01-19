# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HearthstoneCard(models.Model):

    cardId = models.CharField(unique=True,
                              null=False,
                              db_index=True,
                              max_length=32)

    dbfId = models.IntegerField()

    name = models.CharField(max_length=128)

    cardSet = models.CharField(max_length=64)

    type = models.CharField(max_length=64)

    text = models.CharField(max_length=64)

    playerClass = models.CharField(max_length=64)

    locale = models.CharField(max_length=16)