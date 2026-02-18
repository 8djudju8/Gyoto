#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    Copyright 2014 Frederic Vincent, Thibaut Paumard
#
#    This file is part of Gyoto.
#
#    Gyoto is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Gyoto is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Gyoto.  If not, see <http://www.gnu.org/licenses/>.
#
# import os
import time
import unittest
import gyoto.core
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import inspect
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

gyoto.core.requirePlugin('stdplug')

GYOTO_EXAMPLES_DIR = "../../doc/examples/"


class TestStarTrace(unittest.TestCase):
    def test_create_obj_StarTrace(self):
        print("StarTrace Astrobj")
        if gyoto.GYOTO_USE_XERCES:
            sc = gyoto.core.Factory(GYOTO_EXAMPLES_DIR
                                    + "example-moving-star.xml").scenery()
            sc.screen().mask(None)  # make sure no mask is set yet
            st = sc.astrobj()
        else:
            # No XML, build from scratch
            met = gyoto.std.KerrBL()
            st = gyoto.std.Star()
            st.metric(met)
            st.radius(2.)
            st.setInitCoord = ((600., 9., 1.5707999999999999741, 0),
                               (0., 0., 0.037037))
            screen = gyoto.Screen()
            screen.metric(met)
            screen.observerpos = [1000., 100., 0.78, 0.]
            screen.time(1000.)
            screen.resolution(128)
            screen.FieldOfView(0.1 * np.pi)
            sc = gyoto.core.Factory().scenery()
            sc.metric(met)
            sc.screen(screen)
            sc.astrobj(st)
            sc.tmin = 0.

        print("Instanciating StarTrace from Star... ")
        st = gyoto.std.Star(st)
        stt = gyoto.std.StarTrace(st, 600, 800)
        print("done.")

        print("Mutating StarTrace... ")
        stt.set('Adaptive', 0)
        stt.set('Delta', 1.)
        stt.set('OpticallyThin', False)
        print("done.")

        sc.astrobj(stt)
        sc.nThreads(8)

        print("Ray-tracing StarTrace... ")
        tic = time.time()
        sc.set('Quantities', "Intensity")
        mask = sc[:, :]["Intensity"]
        tac = time.time()
        print(f"done. {tac - tic}")
        sc.astrobj(st)

        print("Ray-tracing Star without mask... ")
        tic = time.time()
        im1 = sc[:, :]["Intensity"]
        tac = time.time()
        print(f"done. {tac - tic}")

        pmask=gyoto.core.array_double.fromnumpy2(mask)
        sc.screen().mask(pmask)
        print("Ray-tracing Star with mask... ")
        tic = time.time()
        im2 = sc[:, :]["Intensity"]
        tac = time.time()
        print(f"done. {tac - tic}")
        # TODO plot ? compare im1 im2
        print(" end StarTrace Astrobj")
