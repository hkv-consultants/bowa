# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import datetime
import logging
import os
import random
import shutil
import string
import zipfile
import csv

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

logger = logging.getLogger(__name__)

FIXED_FILENAMES = {
    'ht10': 'ht010.asc',
    'ht25': 'ht025.asc',
    'ht50': 'ht050.asc',
    'ht100': 'ht100.asc',
    'pg': 'pg.asc',
    'lg': 'lg.asc',
    'ah': 'ah.asc',
    'te': 'te.asc',
    'err_matrix': 'err_matrix.txt',
    'normen': 'norment.txt',
}

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
    err_matrix = models.FilePathField(null=True, blank=True)
    normen = models.FilePathField(null=True, blank=True)

    ahdev = models.FloatField(null=True, blank=True)
    htdev = models.FloatField(null=True, blank=True)
    nsim = models.IntegerField(null=True, blank=True)
    rho = models.FloatField(default=0.8)
    scenario_type = models.IntegerField(
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

    def workdir(self):
        return os.path.join(
            settings.BUILDOUT_DIR, 'var', 'bowa', str(self.id))

    def move_files(self, metadata):
        """Function is called when the user has uploaded correct
        files. Metadata has keys 'lg', 'ht10' etc for each field and
        the values have a key 'path' that says where the file
        currently is. Copy it to a directory like
        'var/bowa/<scenario_id>/'."""

        directory = self.workdir()
        os.makedirs(directory)

        for field, data in metadata.items():
            fixed_filename = FIXED_FILENAMES[field]
            target = os.path.join(directory, fixed_filename)
            if data['path'].lower().endswith('.zip'):
                zipf = zipfile.ZipFile(data['path'], 'r')
                for zipinfo in zipf.infolist():
                    zipinfo.filename = fixed_filename
                    zipf.extract(zipinfo, directory)
                    break  # Zip files are supposed to contain a single file
            else:
                shutil.copyfile(data['path'], target)
            setattr(self, field, target)

        self.save()

    def run_r(self):
        cmd = ("R CMD BATCH --no-save --no-restore '--args {workdir} {nsim} {ahdev} {htdev} {rho}' {r_script}"
            .format(
                workdir=self.workdir(), nsim=self.nsim, ahdev=self.ahdev, htdev=self.htdev, rho=self.rho,
                r_script="/vagrant/linux_sources/downloads/test/bowa.r"
            ))
        logger.debug("Running {}".format(cmd))
        os.system(cmd)

    def csv_of_result_file(self):
        result = os.path.join(self.workdir(), 'resultaat.txt')
        if not os.path.exists(result):
            return ''
        else:
            # Open the CSV file for reading
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def list_of_toetseenheden(self):
	# sql <- "SELECT toetseenheid from resultaat WHERE percentage > 0"
        result = os.path.join(self.workdir(), 'resultaat.db')
        if not os.path.exists(result):
            return ''
        else:
            # Open the database
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def list_of_grondgebruiken(self):
        result = os.path.join(self.workdir(), 'resultaat.db')
        if not os.path.exists(result):
            return ''
        else:
            # Open the database
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def list_of_normfuncties(self):
        result = os.path.join(self.workdir(), 'resultaat.db')
        if not os.path.exists(result):
            return ''
        else:
            # Open the database
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def list_of_presentaties(self):
        result = os.path.join(self.workdir(), 'resultaat.db')
        if not os.path.exists(result):
            return ''
        else:
            # Open the database
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def __unicode__(self):
        return self.name
