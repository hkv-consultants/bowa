# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import datetime
import random
import string

from django.db import models
from django.core.urlresolvers import reverse


class BowaScenario(models.Model):
    SCENARIO_TYPES = (
        (1, "Simulaties"),
        (2, "NBW Toetsing"))

    name = models.CharField(max_length=100)
    email = models.EmailField()

    ht10 = models.FilePathField(null=True, blank=True)
    ht25 = models.FilePathField(null=True, blank=True)
    ht50 = models.FilePathField(null=True, blank=True)
    ht100 = models.FilePathField(null=True, blank=True)
    pg = models.FilePathField(null=True, blank=True)
    lg = models.FilePathField(null=True, blank=True)
    ah = models.FilePathField(null=True, blank=True)
    te = models.FilePathField(null=True, blank=True)

    deviation_ah = models.FloatField(null=True, blank=True)
    deviation_h = models.FloatField(null=True, blank=True)
    num_simulations = models.IntegerField(null=True, blank=True)
    scenario_types = models.IntegerField(
        null=True, blank=True, choices=SCENARIO_TYPES)

    slug = models.SlugField(
        null=True, blank=True,
        help_text='auto generated on save; used for url')

    datetime_created = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ''.join(random.sample(string.letters, 20))
        if not self.expiration_date:
            self.expiration_date = (
                datetime.datetime.now() + datetime.timedelta(days=7))

        return super(BowaScenario, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('bowa_result', kwargs=dict(slug=self.slug))

    def __unicode__(self):
        return self.name
