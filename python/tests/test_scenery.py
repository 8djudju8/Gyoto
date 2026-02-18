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
import os
import unittest
import time as tps
import gyoto.core
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import inspect
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

gyoto.core.requirePlugin('stdplug')

GYOTO_EXAMPLES_DIR = "../../doc/examples/"


class TestScenery(unittest.TestCase):
    def test_create_obj_Scenery(self):

        print("Scenery")

        # // From yutils, for tic() and tac()
        # include "util_fr.i"

        print("New scenery... ")
        sc = gyoto.core.Scenery()
        print("done.")

        print("Printing this Scenery:")
        print(f"{sc}")

        print(f"Pointer to this Scenery: {sc.getPointer=}")

        # // MaxIter is a property of type size_t. The implementation of such
        # // properties rely on undefined behaviour. Check here that it works
        # // practice. If one of these test fail, we have to find a new
        # // implementation of GYOTO_PROPERTY_SIZE_T.

        print("Using maxiter()")
        max1 = sc.maxiter()
        print(max1)
        print("Using MaxIter()")
        max2 = sc._maxiter()
        print(max2)

        print("Comparing")
        if (max1 != max2):
            print("error maxiter() and MaxIter() do not yield the same value")

        print("Checking MaxIter(val)")
        sc.maxiter(25)
        print(sc.maxiter)
        print(sc.maxiter())
        print(sc._maxiter())
        print("lui none")
        print(sc.maxiter(25))
        print(sc._maxiter())
        if ((sc.maxiter()) != 25):
            print("error MaxIter and maxiter do not agree")

        sc._maxiter(40)
        print("Checking maxiter(val)")
        if ((sc._maxiter()) != 40):
            print("error, MaxIter and maxiter do not agree")

        # // Set back the original value. Phew, GYOTO_PROPERTY_SIZE_T works as
        # // expected.
        sc.maxiter(max1)

        print("New scenery, setting only \"time\"... ")
        sc2 = gyoto.core.Scenery()
        scr = gyoto.core.Screen()
        scr.time(1)
        # sc2.time(1)

        print("Printing this Scenery:")
        print(sc2)
        print(f"Pointer to this Scenery: {sc2.getPointer()=}")

        print("attaching metric to scenery... ")
        gg = gyoto.core.Metric("KerrBL")
        sc.metric(gg)
        print("done.")

        print("Printing this Scenery:")
        print(sc)
        print("Pointer to this Scenery: ")
        print(f"Pointer to this Scenery: {sc.getPointer()=}")

        print("Creating star... ")
        ao = gyoto.std.Star()
        ao.metric(gg)
        ao.radius(0.5)
        ao.setInitCoord((0, 6, np.pi / 2., 0), (0, 1e-3, 0))
        print("done.")

        print("Attaching astrobj to scenery... ")
        sc.astrobj(ao)

        print("Retrieving astrobj... ")
        ao2 = sc.astrobj()
        print(f"Pointer to this astrobj: {ao2.getPointer()=}")
        print("done.")

        print("Setting time... ")
        sc.screen().time(10000)
        print("done.")
        print(f"{sc.screen().time()=}")
        time2 = sc.screen().time()
        if (time2 != 10000):
            print("error CHECK FAILED")

        #  print "Setting tmin... "
        #  rien=sc(screen=)(tmin=-10000)
        #  print "done."
        #  "Checking tmin:", (tmin=sc(screen=)(get_tmin=1))
        #  if (tmin!=-10000) error, "CHECK FAILED"

        #  print "Setting dtau... "
        #  sc, dtau=0.1
        #  print "done."
        #  "Checking dtau:", (dtau=sc(get_dtau=1))
        #  if (dtau!=0.1) error, "CHECK FAILED"

        print("Setting field-of-view... ")
        sc.screen().fieldOfView(np.pi / 4.)
        print("done.")
        print(f"{sc.screen().fieldOfView()=}")
        fov = sc.screen().fieldOfView()
        if (fov != np.pi / 4):
            print("error CHECK FAILED")

        print("Setting resolution... ")
        sc.screen().resolution(16)
        print("done.")
        res = sc.screen().resolution()
        if (res != 16):
            print("error CHECK FAILED")

        print("Setting inclination... ")
        sc.screen().inclination(np.pi / 3.)
        print("done.")
        print("Checking inclination:")
        incl = sc.screen().inclination()
        if (incl != np.pi / 3):
            print("error CHECK FAILED")

        if gyoto.GYOTO_USE_XERCES:
            print("Writing XML description... ")
            gyoto.core.Factory(sc).write("test.xml")
            os.remove("test.xml")

            print("Reading Scenery from XML description... ")
            sc3 = gyoto.core.Factory(GYOTO_EXAMPLES_DIR +
                                     "example-moving-star.xml").scenery()
        print("creating scenery from scratch... ")
        gg = gyoto.std.KerrBL()
        spectro = gyoto.spectrometer.Uniform()
        # TODO spectro uniform = wave ?
        spectro.nSamples(1)
        spectro.band = [2e-6, 2.4e-6]
        scr = gyoto.core.Screen()
        scr.metric(gg)
        scr.setObserverPos([1000., 100., 0.78, 0.])
        scr.time(1000.)
        scr.resolution(128)
        scr.spectrometer(spectro)
        ao = gyoto.std.Star()
        ao.metric(gg)
        ao.radius(2)
        ao.rMax(50)
        ao.setInitCoord((600, 9, 1.5707999999999999741, 0), (0., 0., 0.037037))
        sc3 = gyoto.core.Scenery()
        sc3.metric(gg)
        sc3.screen(scr)
        sc3.astrobj(ao)
        sc3.tMin(0.)
        sc3.screen().resolution(32)
        sc3.astrobj().set("Radius", 2.)
        print("done.")

        print("Ray-tracing on 1 thread (sc())... \n")
        sc3.nThreads(1)
        tic = tps.time()
        sc3.requestedQuantitiesString('Intensity EmissionTime MinDistance')
        im1 = sc3.rayTrace()  # [:, :]   , "Intensity"]    raytrace
        # Or we can do it manually to understand how the Gyoto API works:

        res = sc.screen().resolution()
        intensity = np.zeros((res, res), dtype=float)
        time = np.zeros((res, res), dtype=float)
        distance = np.zeros((res, res), dtype=float)
        aop = gyoto.core.AstrobjProperties()

        aop.intensity = gyoto.core.array_double.fromnumpy2(intensity)
        aop.time = gyoto.core.array_double.fromnumpy2(time)
        aop.distance = gyoto.core.array_double.fromnumpy2(distance)

        ii = gyoto.core.Range(1, res, 1)
        jj = gyoto.core.Range(1, res, 1)
        grid = gyoto.core.Grid(ii, jj, "\rj = ")

        sc.rayTrace(grid, aop)
        tac = tps.time()
        print(f"done in {tac - tic}")
        plt.imshow(intensity)
        # pli, im1
        # pause, 1000
        print("done.")
        print(f"{sc3.screen().resolution()=}")
        print("Ray-tracing on 2 threads (sc())... \n")
        sc3.nThreads(2)
        tic = tps.time()
        im1 = sc3[15, 15]  # raytrace
        tac = tps.time()
        print(f"done in {tac - tic}")
        print(f"{type(im1)=}")
        # print(f"{im1.shape=}")
        print(f"{im1=}")
        # plt.imshow(im1['Intensity'])
        print("done.")

        print("Ray-tracing on 2 threads (gyoto_Scenery_rayTrace())... \n")
        sc3.nThreads(2)
        # sc3.quantities("Intensity")
        sc3.requestedQuantitiesString("Intensity")
        im1 = sc3.rayTrace()
        plt.imshow(im1['Intensity'])
        print("done.")

        print("Ray-tracing on 1 thread... \n")
        sc3.nThreads(1)
        tic = tps.time()
        mask = sc3.rayTrace()
        tac = tps.time()
        print(f"done in {tac - tic}")
        print("done.")

        print("Setting mask... ")
        sc3.screen().mask(mask)

        print("Checking mask... ")
        mask2 = sc3.screen().mask()
        if not all(mask2 == mask):
            print("error CHECK FAILED!")

        print("Ray-tracing on 1 thread with mask... \n")
        sc3.nthreads(1)
        tic = tps.time()
        im1 = sc3.rayTrace()
        tac = tps.time()
        if not all(im1 == mask):
            print("error CHECK FAILED!")
        print(f"done in {tac - tic}")

        print("Ray-tracing with mask (sc())... \n")
        sc3.nthreads(1)
        tic = tps.time()
        im1 = sc3[:, :, "Intensity"]  # raytrace
        if (not all(im1 == mask)):
            print("error CHECK FAILED!")
        tac = tps.time()
        plt.imshow(im1['Intensity'])
        print(f"done in {tac - tic}")

        # //noop,sc3.screen(maskwrite="toto.fits")
        # //noop,sc3.screen(xmlwrite="toto.xml")

        # /* print "Ray-tracing on adaptive grid... "
        # data = gyoto_Scenery_adaptive_raytrace(sc3, 4)
        # fma
        # pli, data(,,3), cmax=100
        # write, format="%s\n" , "done."; */

        print("Cloning...")
        sc4 = sc3.clone()
        print("DONE.")

        print("Printing clone:")
        print(sc4)

        ph = gyoto.core.Photon()
        ph.initcoord(sc3, 6, 19)
        ph.hit()

        print("Reading Scenery from XML description... ")
        sc = gyoto.core.Factory(GYOTO_EXAMPLES_DIR +
                                "example-complex-astrobj.xml").scenery()

        sc.nthreads(8)
        sc.nprocesses(0)
        sc.mpispawn(0)

        print("Integrating whole field...")
        data = sc[:, :]

        r1 = "8:25:4"
        r2 = "2:-2:3"
        v1 = [1, 4, 16]
        v2 = [15, 20, 22]
        s1 = [[1, 2], [3, 4]]
        s2 = [[[12, 13], [14, 15]],
              [[1, 2], [3, 4]],
              [[10, 11], [16, 17]],
              [[7, 8], [20, 22]]]

        print("Integrating subfield...")
        data2 = sc[r1, r2, :]

        print("Comparing...")
        if (any(data2 != data[r1, r2, :])):
            print("error result differ")

        print("Integrating subfield...")
        data2 = sc[v1, v2, :]

        print("Comparing...")
        if (any(data2 != data[v1, v2, :])):
            print("error result differ")

        print("Integrating subfield...")
        data2 = sc[s1, s2, :]

        print("Comparing...")
        if (any(data2 != data[s1, s2, :])):
            print("error result differ")

        print("Integrating subfield...")
        data2 = sc[r1, v2, :]

        print("Comparing...")
        if (any(data2 != data[r1, v2, :])):
            print("error result differ")

        print("Integrating subfield...")
        data2 = sc[v1, r2, :]

        print("Comparing...")
        if (any(data2 != data[v1, r2, :])):
            print("error result differ")

        fov = sc.screen().fieldOfView()
        npix = sc.screen().resolution()
        delta = fov / float(npix)

        # verifie
        tmp = (np.arange(1, npix + 1) - 0.5) * delta - fov / 2.
        xx = np.tile(tmp, (32, 1))
        # xx=((indgen(npix)-0.5)*delta-fov/2.)(, -:1:32)
        yy = np.transpose(xx)

        data2 = np.ones((npix, npix))
        print("integrating pix. by pix., specifying angles...\n")
        # verbosity = gyoto.verbose(0)
        for j in range(npix):
            print(f"{j}=, {npix}=")
            for i in range(npix):
                data2[i, j, 0] = sc[-xx[i, j], yy[i, j], :]

        print("Comparing results")
        diff = data - data2
        ind = np.where(data)
        diff[ind] /= data[ind]
        mdiff = max(abs(diff))
        if (mdiff > 1e-6):
            print("error Results differ")
        print(f"OK (max rel. dif.: {mdiff=}")

        print("integrating whole field, specifying angles...\n")
        data2 = sc[-xx, yy, :]

        print("Comparing results")
        diff = data - data2
        ind = np.where(data)
        diff[ind] /= data[ind]
        mdiff = max(abs(diff))
        if (mdiff > 1e-6):
            print("error Results differ")
        print(f"OK (max rel. dif.: {mdiff=}")

        # if (batch()) {

        # // Free memory for easier checking with valgrind
        # xx=yy=data2=data=ind=[]
        # sc4=[]
        # sc3=[]
        # sc2=[]
        # sc=[]
        # ao=ao2=[]
        # pause, 1000
        # winkill
        # }
        print("End Scenery")

    def test_load_save_Scenery(self):

        print("Scenery")

        # // From yutils, for tic() and tac()
        # include "util_fr.i"

        print("New scenery... ")
        sc = gyoto.core.Scenery()
        print("done.")

        print("Printing this Scenery:")
        print(f"{sc}")


if __name__ == '__main__':
    unittest.main()
