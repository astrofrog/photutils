# Licensed under a 3-clause BSD style license - see LICENSE.rst

# The functions defined here allow one to determine the exact area of
# overlap of an ellipse and a triangle (written by Thomas Robitaille).
# The approach is to divide the rectangle into two triangles, and
# reproject these so that the ellipse is a unit circle, then compute the
# intersection of a triagnel with a unit circle.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np
cimport numpy as np

__all__ = ['elliptical_overlap_grid']

cdef extern from "math.h":

    double asin(double x)
    double sin(double x)
    double cos(double x)
    double sqrt(double x)

from cpython cimport bool

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cimport cython

from .core import distance, area_triangle, overlap_area_triangle_unit_circle


def elliptical_overlap_grid(double xmin, double xmax, double ymin, double ymax,
                            int nx, int ny, double rx, double ry, double theta,
                            int use_exact, int subpixels):
    """
    elliptical_overlap_grid(x, y, dx, dy, theta)

    Area of overlap between an ellipse and a pixelgrid.
    Given a grid with walls set by x, y, find the fraction of overlap in
    each with an ellipse with major and minor axes dx and dy
    respectively, position angle theta, and centered at the origin.
    The ellipse is centered on the 0,0 position.

    Parameters
    ----------
    xmin, xmax, ymin, ymax : float
        Extent of the grid in x and y direction.
    nx, ny : int
        Dimension of grid.
    rx : float
        The semimajor axis.
    ry : float
        The semiminor axis.
    theta : float
        The position angle of the semimajor axis in radians (counterclockwise)
    use_exact : 0 or 1
        If ``1`` calculates exact overlap, if ``0`` uses ``subpixel`` number
        of subpixels to calculate the overlap.
    subpixels : int
        Each pixel resampled by this factor in each dimension, thus each
        pixel is devided into ``subpixels ** 2`` subpixels.

    Returns
    -------
    frac : `~numpy.ndarray`
        2-d array giving the fraction of the overlap.
    """

    cdef unsigned int i, j
    cdef double x, y, dx, dy
    cdef double bxmin, bxmax, bymin, bymax
    cdef double pxmin, pxmax, pymin, pymax

    # Define output array
    cdef np.ndarray[DTYPE_t, ndim=2] frac = np.zeros([ny, nx], dtype=DTYPE)

    # Find the width of each element in x and y
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny

    # For now we use a bounding circle and then use that to find a bounding box
    # but of course this is inefficient and could be done better.

    # Find bounding circle radius
    R = max(rx, ry)

    # Define bounding box
    bxmin = -R - 0.5 * dx
    bxmax = +R + 0.5 * dx
    bymin = -R - 0.5 * dy
    bymax = +R + 0.5 * dy

    for i in range(nx):
        pxmin = xmin + i * dx  # lower end of pixel
        pxmax = pxmin + dx  # upper end of pixel
        if pxmax > bxmin and pxmin < bxmax:
            for j in range(ny):
                pymin = ymin + j * dy
                pymax = pymin + dy
                if pymax > bymin and pymin < bymax:
                    if use_exact:
                        frac[j, i] = elliptical_overlap_single_exact(pxmin, pymin, pxmax, pymax, rx, ry, theta) / (dx * dy)
                    else:
                        frac[j, i] = elliptical_overlap_single_subpixel(pxmin, pymin, pxmax, pymax, rx, ry, theta, subpixels) / (dx * dy) 

    return frac


def elliptical_overlap_single_subpixel(double x0, double y0,
                                       double x1, double y1,
                                       double rx, double ry,
                                       double theta, int subpixels):
    """
    Return the fraction of overlap between a ellipse and a single pixel with
    given extent, using a sub-pixel sampling method.
    """

    cdef unsigned int i, j
    cdef double x, y
    cdef double frac = 0.  # Accumulator.
    cdef double rx_sq, ry_sq
    cdef double cos_theta = cos(theta)
    cdef double sin_theta = sin(theta)

    dx = (x1 - x0) / subpixels
    dy = (y1 - y0) / subpixels
    
    rx_sq = rx * rx
    ry_sq = ry * ry
    
    x = x0 - 0.5 * dx
    for i in range(subpixels):
        x += dx
        y = y0 - 0.5 * dy
        for j in range(subpixels):
            y += dy
            
            # Transform into frame of rotated ellipse
            x_tr = y * sin_theta + x * cos_theta
            y_tr = y * cos_theta - x * sin_theta

            if x_tr * x_tr / rx_sq + y_tr * y_tr / ry_sq < 1:
                frac += 1.

    return frac / (subpixels * subpixels)


def elliptical_overlap_single_exact(double xmin, double ymin,
                                    double xmax, double ymax,
                                    double rx, double ry,
                                    double theta):
    """
    Given a rectangle defined by (xmin, ymin, xmax, ymax) and an ellipse
    with major and minor axes rx and ry respectively, position angle theta,
    and centered at the origin, find the area of overlap.
    """

    cdef double cos_m_theta = cos(-theta)
    cdef double sin_m_theta = sin(-theta)
    cdef double scale

    # Find scale by which the areas will be shrunk
    scale = rx * ry

    # Reproject rectangle to frame of reference in which ellipse is a unit circle
    x1, y1 = (xmin * cos_m_theta - ymin * sin_m_theta) / rx, (xmin * sin_m_theta + ymin * cos_m_theta) / ry
    x2, y2 = (xmax * cos_m_theta - ymin * sin_m_theta) / rx, (xmax * sin_m_theta + ymin * cos_m_theta) / ry
    x3, y3 = (xmax * cos_m_theta - ymax * sin_m_theta) / rx, (xmax * sin_m_theta + ymax * cos_m_theta) / ry
    x4, y4 = (xmin * cos_m_theta - ymax * sin_m_theta) / rx, (xmin * sin_m_theta + ymax * cos_m_theta) / ry

    # Divide resulting quadrilateral into two triangles and find intersection with unit circle
    return (overlap_area_triangle_unit_circle(x1, y1, x2, y2, x3, y3) \
          + overlap_area_triangle_unit_circle(x1, y1, x4, y4, x3, y3)) \
          * scale

