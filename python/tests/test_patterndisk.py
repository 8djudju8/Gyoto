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
import sys
import unittest
import gyoto.core
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import inspect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

gyoto.core.requirePlugin('stdplug')
# GYOTO_PYTHON_DIR = "./"
# GYOTO_EXAMPLES_DIR = GYOTO_PYTHON_DIR + "../doc/examples/"
GYOTO_ARTIFACTS_DIR = "./tests/artifacts/"


class TestPatternDisk(unittest.TestCase):
    def test_create_obj_PatternDisk(self):
        # gyoto.core.debug(1)
        gyoto.core.verbose(10)
        print(f"path {sys.argv[0]=}")
        dirname, filename = os.path.split(os.path.abspath(__file__))
        print(f"running from {dirname}")
        print(f"file is {filename}")

        print("PatternDisk Astrobj")
        # Create a metric
        metric = gyoto.std.KerrBL()
        metric.mass(4e6, "sunmass")
        # Create PatternDisk
        # Create opacity and intensity grids as numpy arrays.
        # Get pointers in a format that Gyoto understands.
        # Warning: here we assume that size_t is the same as uint64.
        gridshape = np.asarray((1, 3, 11), np.uint64)
        pgridshape = gyoto.core.array_size_t.fromnumpy1(gridshape)
        opacity = np.zeros(gridshape)
        popacity = gyoto.core.array_double.fromnumpy3(opacity)
        opacity[:, 0::2, 0::2] = 100.
        opacity[:, 1::2, 1::2] = 100.
        intensity = opacity * 0. + 1.
        pintensity = gyoto.core.array_double.fromnumpy3(intensity)
        # Create PatternDisk, attach grids, set some parameters
        pd = gyoto.std.PatternDisk()
        pd.copyIntensity(pintensity, pgridshape)
        pd.copyOpacity(popacity, pgridshape)
        pd.innerRadius(3)
        pd.outerRadius(28)
        pd.repeatPhi(8)
        pd.metric(metric)
        pd.rMax(50)
        # Create screen
        screen = gyoto.core.Screen()
        screen.metric(metric)
        screen.resolution(64)
        screen.time(1000., "geometrical_time")
        screen.distance(100., "geometrical")
        screen.fieldOfView(30. / 100.)
        screen.inclination(110., "degree")
        screen.PALN(180., "degree")
        # Create Scenery
        sc = gyoto.core.Scenery()
        sc.metric(metric)
        sc.screen(screen)
        sc.astrobj(pd)

        # simple save fits
        print("========= FISRT CASE simple save fits")
        pd.fitsWrite("!check-patterndisk.fits.gz")
        print("fitswrite ok")
        # simple Save Scenery
        print("simple save scenery")
        gyoto.core.Factory(sc).write("check-patterndisk.xml")
        print("factory write ok")
        # simple Read Scenery
        gyoto.core.Factory("check-patterndisk.xml").scenery()
        print("factory scenery read ok")
        os.unlink("check-patterndisk.fits.gz")
        os.unlink("check-patterndisk.xml")

        # Save fits same directory
        print("========= SECOND CASE save fits same dir tire par les cheveux")
        # si pd fitswrite and save factory should update fillproperty filename
        # order is important
        # pd.fitsWrite("!" + GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        print("fitswrite ok")
        # Save Scenery same directory
        print("save scenery fits xml same directory")
        gyoto.core.Factory(sc).write(GYOTO_ARTIFACTS_DIR
                                     + "check-patterndisk.xml")
#        gyoto.core.Factory(sc).write("check-patterndisk.xml")
        pd.fitsWrite("!" + GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")

        print("factory write ok")
        # Read Scenery same directory
        sc2 = gyoto.core.Factory(GYOTO_ARTIFACTS_DIR
                                 + "check-patterndisk.xml").scenery()
        print("factory scenery read ok")
        # Check
        # Compare Sceneries
        self.assertEqual(sc2.screen().dMax(), sc.screen().dMax(),
                         "dmax was not conserved when RW XML file")
        self.assertEqual(sc2.tMin(), sc.tMin(),
                         "tmin was not conserved when RW XML file")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk.xml")

        # Save Scenery different path
        print("========= THIRD CASE save scenery fits xml different directory")
        # pd.fitsWrite("!" + GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        # pd.fitsWrite("check-patterndisk.fits.gz", "LALLAL")
        pd.fitsWrite("check-patterndisk.fits.gz", "!" + GYOTO_ARTIFACTS_DIR)
        print("fitswrite ok")
        gyoto.core.Factory(sc).write("check-patterndisk.xml")
        print("factory write ok")
        # Read Scenery
        gyoto.core.Factory("check-patterndisk.xml").scenery()
        print("factory scenery read ok")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        os.unlink("check-patterndisk.xml")

        # Save Scenery different path
        print("========= FOURTH CASE save scenery fits xml diff directory")
        pd.fitsWrite("!check-patterndisk.fits.gz")
        print("fitswrite ok")
        gyoto.core.Factory(sc).write(GYOTO_ARTIFACTS_DIR +
                                     "check-patterndisk.xml")
        print("factory write ok")
        # Read Scenery
        gyoto.core.Factory(GYOTO_ARTIFACTS_DIR +
                           "check-patterndisk.xml").scenery()
        print("factory scenery read ok")

        # Delete temporary files
        os.unlink("check-patterndisk.fits.gz")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk.xml")

        # Compare PatternDisks
        # compare shape
        pd2 = gyoto.std.PatternDisk(sc2.astrobj())
        pgridshape2 = gyoto.core.array_size_t(3)
        pd2.getIntensityNaxes(pgridshape2)
        for k in range(3):
            assert pgridshape2[k] == pgridshape[k], "shape of grid changed"
        bufsize = gridshape.prod()
        # compare intensity
        buf = gyoto.core.array_double.frompointer(pd2.getIntensity())
        for k in range(bufsize):
            # np.testing.assert_almost_equal(buf[k], pintensity[k])
            assert buf[k] == pintensity[k], "Intensity changed"
        # compare opacity
        buf = gyoto.core.array_double.frompointer(pd2.opacity())
        for k in range(bufsize):
            assert buf[k] == popacity[k], "Opacity changed"
#                self.assertTrue(False)
        file_output = PdfPages(GYOTO_ARTIFACTS_DIR + "check-patterndisk.pdf")
        # Ray-trace
        ii = gyoto.core.Range(1, screen.resolution(), 1)
        jj = gyoto.core.Range(1, screen.resolution(), 1)
        grid = gyoto.core.Grid(ii, jj)
        aop = gyoto.core.AstrobjProperties()
        frame = np.zeros((screen.resolution(), screen.resolution()))
        pframe = gyoto.core.array_double.fromnumpy2(frame)
        aop.intensity = pframe
        sc.rayTrace(grid, aop)
        plt.figure()
        plt.imshow(frame, origin='lower')
        # plt.savefig(frame)
        file_output.savefig()
        plt.close()
        file_output.close()
        # plt.imshow(frame, origin='lower')
        # plt.show()
        print("PatternDisk Astrobj done")

    @unittest.expectedFailure
    def test_create_obj_assert(self):
        self.assertTrue(False)
#
#    def test_create_obj_assertTrue(self):
#        assert True


if __name__ == '__main__':
    unittest.main()
