import random

import numpy as np

from photutils.aperture import CircularAperture, \
                               CircularAnnulus, \
                               EllipticalAperture, \
                               EllipticalAnnulus


NITER = 100

random.seed('generate_regression')


def sample_grid(r):
    xmin = random.uniform(-10., -r)
    xmax = random.uniform(+r, +10.)
    ymin = random.uniform(-10., -r)
    ymax = random.uniform(+r, +10.)
    nx = int(round(random.uniform(1, 100)))
    ny = int(round(random.uniform(1, 100)))
    return xmin, xmax, ymin, ymax, nx, ny

f = open('data/reference_circular.txt', 'wb')
for i in range(NITER):
    r = random.uniform(0., 10.)
    ap = CircularAperture(r)
    f.write('%20.16f' % r)
    xmin, xmax, ymin, ymax, nx, ny = sample_grid(r)
    f.write(' %20.16f %20.16f %20.16f %20.16f %3i %3i' % (xmin, xmax, ymin, ymax, nx, ny))
    for subpixel in [1, 2, 5, 10, 20]:
        frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
        f.write(' %14.5f' % np.sum(frac))
    f.write('\n')
f.close()

f = open('data/reference_circular_annulus.txt', 'wb')
for i in range(NITER):
    r1 = random.uniform(0., 10.)
    r2 = random.uniform(r1, 10.)
    ap = CircularAnnulus(r1, r2)
    f.write('%20.16f %20.16f' % (r1, r2))
    xmin, xmax, ymin, ymax, nx, ny = sample_grid(r)
    f.write(' %20.16f %20.16f %20.16f %20.16f %3i %3i' % (xmin, xmax, ymin, ymax, nx, ny))
    for subpixel in [1, 2, 5, 10, 20]:
        frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
        f.write(' %14.5f' % np.sum(frac))
    f.write('\n')
f.close()

f = open('data/reference_elliptical.txt', 'wb')
for i in range(NITER):
    a = random.uniform(0., 10.)
    b = random.uniform(0., a)
    theta = random.uniform(0., 2. * np.pi)
    ap = EllipticalAperture(a, b, theta)
    f.write('%20.16f %20.16f %20.16f' % (a, b, theta))
    xmin, xmax, ymin, ymax, nx, ny = sample_grid(r)
    f.write(' %20.16f %20.16f %20.16f %20.16f %3i %3i' % (xmin, xmax, ymin, ymax, nx, ny))
    for subpixel in [1, 2, 5, 10, 20]:
        frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
        f.write(' %14.5f' % np.sum(frac))
    f.write('\n')
f.close()

f = open('data/reference_elliptical_annulus.txt', 'wb')
for i in range(NITER):
    a_in = random.uniform(0., 10.)
    a_out = random.uniform(a_in, 10.)
    b_out = random.uniform(0., a_out)
    theta = random.uniform(0., 2. * np.pi)
    ap = EllipticalAnnulus(a_in, a_out, b_out, theta)
    f.write('%20.16f %20.16f %20.16f %20.16f' % (a_in, a_out, b_out, theta))
    xmin, xmax, ymin, ymax, nx, ny = sample_grid(r)
    f.write(' %20.16f %20.16f %20.16f %20.16f %3i %3i' % (xmin, xmax, ymin, ymax, nx, ny))
    for subpixel in [1, 2, 5, 10, 20]:
        frac = ap.encloses(xmin, xmax, ymin, ymax, nx, ny, method='subpixel', subpixels=subpixel)
        f.write(' %14.5f' % np.sum(frac))
    f.write('\n')
f.close()
