import random

import numpy as np

from ..aperture import CircularAperture, \
                       CircularAnnulus, \
                       EllipticalAperture, \
                       EllipticalAnnulus
import os

from numpy.testing import assert_array_almost_equal_nulp

ROOT = os.path.dirname(__file__)

def test_accuracy_circular_subpixel():
    
    for line in open(ROOT + '/data/reference_circular.txt', 'rb'):

        values = [float(x) for x in line.split()]
        r = values[0]
        xmin, xmax, ymin, ymax = values[1:5]
        nx, ny = int(round(values[5])), int(round(values[6]))
        ref_values = values[-5:]

        ap = CircularAperture(r)
        for i, subpixel in enumerate([1, 2, 5, 10, 20]):
            frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
            assert_array_almost_equal_nulp(np.sum(frac), ref_values[i], 20)


def test_accuracy_circular_annulus_subpixel():

    for line in open(ROOT + '/data/reference_circular_annulus.txt', 'rb'):

        values = [float(x) for x in line.split()]
        r1, r2 = values[0], values[1]
        xmin, xmax, ymin, ymax = values[2:6]
        nx, ny = int(round(values[6])), int(round(values[7]))
        ref_values = values[-5:]

        ap = CircularAnnulus(r1, r2)
        for i, subpixel in enumerate([1, 2, 5, 10, 20]):
            frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
            assert_array_almost_equal_nulp(np.sum(frac), ref_values[i], 20)


def test_accuracy_elliptical_subpixel():

    for line in open(ROOT + '/data/reference_elliptical.txt', 'rb'):

        values = [float(x) for x in line.split()]
        a, b, theta = values[0:3]
        xmin, xmax, ymin, ymax = values[3:7]
        nx, ny = int(round(values[7])), int(round(values[8]))
        ref_values = values[-5:]

        ap = EllipticalAperture(a, b, theta)
        for i, subpixel in enumerate([1, 2, 5, 10, 20]):
            frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
            assert_array_almost_equal_nulp(np.sum(frac), ref_values[i], 20)


def test_accuracy_elliptical_annulus_subpixel():

    for line in open(ROOT + '/data/reference_elliptical_annulus.txt', 'rb'):

        values = [float(x) for x in line.split()]
        a_in, a_out, b_out, theta = values[0:4]
        xmin, xmax, ymin, ymax = values[4:8]
        nx, ny = int(round(values[8])), int(round(values[9]))
        ref_values = values[-5:]

        ap = EllipticalAnnulus(a_in, a_out, b_out, theta)
        for i, subpixel in enumerate([1, 2, 5, 10, 20]):
            frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
            assert_array_almost_equal_nulp(np.sum(frac), ref_values[i], 20)
