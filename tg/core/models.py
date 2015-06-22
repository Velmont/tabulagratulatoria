from __future__ import unicode_literals

from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField


class Entry(models.Model):
    STATUS = Choices('new', 'checked', 'deleted')

    status = StatusField()
    shown_name = models.CharField(max_length=255, blank=True, default='')

    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')

    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=32, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    postnummer = models.ForeignKey('Postnummer', null=True)
    place = models.CharField(max_length=64, blank=True, default='')

    want_tg = models.BooleanField(default=False)
    num_issues = models.PositiveSmallIntegerField(default=False)

    notes = models.TextField(blank=True, default='')
    groups = models.ManyToManyField('Group', blank=True)

    @property
    def printed_name(self):
        if self.shown_name:
            return self.shown_name
        return self.contact_full_name

    @property
    def contact_full_name(self):
        return "{s.first_name} {s.last_name}".format(s=self)

    class Meta:
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return "{s.printed_name} ({s.status})".format(s=self)


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


class Group(models.Model):
    category = models.SlugField()
    name = models.SlugField()

    @property
    def slug(self):
        return "{s.category}:{s.name}".format(s=self)

    def __unicode__(self):
        return self.slug
