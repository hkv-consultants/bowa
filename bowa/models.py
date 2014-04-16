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

import numpy as np
import Image

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from . import util

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
    'fouten': 'foutenmatrix.txt',
    'normen': 'normen.txt',
}

class BowaScenario(models.Model):
    SCENARIO_TYPES = (
        (1, "NBW toetsing met onzekerheden (simulaties)"),
        (2, "NBW Toetsing zonder onzekerheden"))

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
    fouten = models.FilePathField(null=True, blank=True)
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
            settings.BUILDOUT_DIR, 'var', 'media', 'bowa', str(self.id))

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

    def run_r(self, logger):
	
	if (self.scenario_type == 1):
            cmd = ("R --vanilla --slave --args  {workdir}  {fouten} {normen} {nsim} {ahdev} {htdev} {rho} < {r_script}"
                .format(
                    workdir=self.workdir(), 
                    fouten=FIXED_FILENAMES['fouten'],
                    normen=FIXED_FILENAMES['normen'], 
                    nsim=self.nsim,
                    ahdev=self.ahdev, 
                    htdev=self.htdev,
                    rho=self.rho,
                    r_script=os.path.join(os.path.dirname(__file__), 'r', 'simulatie.R')
                ))
	else:
            cmd = ("R --vanilla --slave --args  {workdir}  {fouten} {normen} < {r_script}"
                .format(
                    workdir=self.workdir(),
                    fouten=FIXED_FILENAMES['fouten'], 
                    normen=FIXED_FILENAMES['normen'], 
                    r_script=os.path.join(os.path.dirname(__file__), 'r', 'nbw_toetsing.R')
                ))

        logger.debug("Running {}".format(cmd))
        os.system(cmd)
        ResultLine.from_csv(self.csv_of_result_file(), self)

    def create_inundation_png(self, asc=None):
        if asc is None:
            asc = os.path.join(
                self.workdir(), 'inundatiekaart.asc')
        if not os.path.exists(asc):
            pass
        
        dataset = util.gdal_open(asc)
        band = dataset.GetRasterBand(1)
        data = band.ReadAsArray()
        shape = data.shape + (4,)

        rgba = np.zeros(shape, np.uint8)
        rgba[:, :, 0] = np.where(
            (data == 2), 255, 0)  # 2 is rood
        rgba[:, :, 1] = np.where(
            (data == 1), 255, 0)  # 1 is groen
        rgba[:, :, 2] = np.where(
            (data == 0), 255, 0)  # 0 is blauw
        rgba[:, :, 3] = np.where(
            (data != band.GetNoDataValue()), 255, 0)  # nodata is transparant

        Image.fromarray(rgba).save(
            os.path.join(self.workdir(), 'inundatiekaart.png'))

    def csv_of_result_file(self):
        result = os.path.join(self.workdir(), 'resultaat.txt')
        if not os.path.exists(result):
            return ''
        else:
            # Open the CSV file for reading
            return list(csv.reader(open(result, 'rb'), delimiter=b'\t'))

    def list_of_toetseenheden(self):
        return sorted(
            value['toetseenheid'] for value in
            self.resultline_set.filter(percentage__gt=0).values('toetseenheid').distinct()
            )

    def list_of_grondgebruiken(self):
        return sorted(
            value['functie'] for value in
            self.resultline_set.filter(percentage__gt=0).values('functie').distinct()
            )
 
    def __unicode__(self):
        return self.name


class ResultLine(models.Model):
    scenario = models.ForeignKey(BowaScenario)

    sim = models.IntegerField()
    toetseenheid = models.IntegerField()
    functie = models.CharField(max_length=50)
    toetshoogte = models.FloatField()
    volume = models.FloatField()
    oppervlakte = models.FloatField()
    percentage = models.FloatField()

    @classmethod
    def from_csv(cls, csv_list, scenario):
        # Throw away existing lines
        scenario.resultline_set.all().delete()
        
        # Add new lines
        for line in csv_list[1:]:
            if len(line) == 6:
                # MBW toetsing scenarios have no sim field,
                # add one.
                line = [0] + line

            cls.objects.create(
                scenario=scenario,
                sim=int(line[0]),
                toetseenheid=int(line[1]),
                functie=line[2],
                toetshoogte=float(line[3]),
                volume=float(line[4]),
                oppervlakte=float(line[5]),
                percentage=float(line[6]))
