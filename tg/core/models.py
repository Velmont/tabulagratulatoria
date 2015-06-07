from __future__ import unicode_literals

from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField


class Entry(models.Model):
    STATUS = Choices('new', 'checked')

    status = StatusField()
    full_name = models.CharField(max_length=255)

    sort_name = models.CharField(max_length=255, blank=True, default='')

    email = models.EmailField(blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    postnummer = models.ForeignKey('Postnummer', null=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return "{s.full_name} ({s.status})".format(s=self)


class Postnummer(models.Model):
    postnr = models.CharField(max_length=6)
    poststad = models.CharField(max_length=50)
    bruksomrade = models.CharField(max_length=50)
    folketal = models.SmallIntegerField(null=True, blank=True)
    bydel = models.CharField(max_length=50)
    kommnr = models.CharField(max_length=50)
    kommune = models.CharField(max_length=50)
    fylke = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    datakvalitet = models.SmallIntegerField()
    sist_oppdatert = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.postnr, self.poststad)
