# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.test import TestCase


import numpy as np

from bowa import models


class TestColorToRgb(TestCase):
    def test_white(self):
        self.assertTrue(
            (models.color_to_rgb("FFFFFF") ==
             np.array([255, 255, 255, 255])).all())


class TestInundationPng(TestCase):
    def test_first_value(self):
        # '5' should get the first color, D7191C = (215, 25, 28)
        rgba = models.colored_image_from_inundation_data(
            np.array([[5, 5], [5, 5]]), 0)

        self.assertTrue(
            (rgba == np.array([[[215, 25, 28, 255],
                                [215, 25, 28, 255]],
                               [[215, 25, 28, 255],
                                [215, 25, 28, 255]]])).all())

    def test_second_value(self):
        # '15' should get the second color
        rgba = models.colored_image_from_inundation_data(
            np.array([[15, 15], [15, 15]]), 0)

        self.assertTrue(
            (rgba == np.array([[[230, 84, 55, 255],
                                [230, 84, 55, 255]],
                               [[230, 84, 55, 255],
                                [230, 84, 55, 255]]])).all())

    def test_last_value(self):
        # '150' should get the last color
        rgba = models.colored_image_from_inundation_data(
            np.array([[150, 150], [150, 150]]), 0)

        self.assertTrue(
            (rgba == np.array([[[43, 131, 186, 255],
                                [43, 131, 186, 255]],
                               [[43, 131, 186, 255],
                                [43, 131, 186, 255]]])).all())

    def test_nodata(self):
        # If nodata, then last value should be 0
        rgba = models.colored_image_from_inundation_data(
            np.array([[150, 150], [150, 150]]), 150)

        self.assertTrue((rgba[:, :, 3] == 0).all())
