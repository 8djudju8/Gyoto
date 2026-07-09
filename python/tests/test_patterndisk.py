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
import copy
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
# GYOTO_ARTIFACTS_DIR = "./tests/artifacts/"
GYOTO_ARTIFACTS_DIR = "./tests/artifacts/"
# GYOTO_XML_DIR = "./tests/artifacts/xml/"
GYOTO_XML_DIR = "./tests/artifacts/xml/"


class TestPatternDisk(unittest.TestCase):

    def create_metric(self):
        # Create a metric
        metric = gyoto.std.KerrBL()
        metric.mass(4e6, "sunmass")
        return metric

    def test_PatternDisk_create(self):
        # gyoto.core.debug(1)
        gyoto.core.verbose(10)
        print(f"path {sys.argv[0]=}")
        dirname, filename = os.path.split(os.path.abspath(__file__))
        print(f"running from {dirname}")
        print(f"file is {filename}")

        print("PatternDisk Astrobj")
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
        metric = self.create_metric()
        # see if we have the good one
        # print(metric.get("Mass"))
        pd.metric(metric)
        pd.rMax(50)
        self.assertIsInstance(pd, gyoto.std.PatternDisk)
        print(f"{gridshape.shape}")
        # needed for tests functions below
        TestPatternDisk.gridshape = gridshape
        TestPatternDisk.pgridshape = pgridshape
        TestPatternDisk.opacity = opacity
        TestPatternDisk.popacity = popacity
        TestPatternDisk.intensity = intensity
        TestPatternDisk.pintensity = pintensity
        TestPatternDisk.pd = pd

    def create_screen(self):
        # Create screen
        screen = gyoto.core.Screen()
        metric = self.create_metric()
        screen.metric(metric)
        screen.resolution(64)
        screen.time(1000., "geometrical_time")
        screen.distance(100., "geometrical")
        screen.fieldOfView(30. / 100.)
        screen.inclination(110., "degree")
        screen.PALN(180., "degree")
        return screen

    def create_scenery(self):
        # Create Scenery
        # print("Create Scenery____________________________")
        sc = gyoto.core.Scenery()
        metric = TestPatternDisk.create_metric(self)
        sc.metric(metric)
        sc.screen(TestPatternDisk.create_screen(self))
        sc.astrobj(TestPatternDisk.pd)

    def test_PatternDisk_create_scenery(self):
        # Create Scenery
        sc = gyoto.core.Scenery()
        metric = self.create_metric()
        sc.metric(metric)
        sc.screen(self.create_screen())
        sc.astrobj(self.pd)
        self.assertIsInstance(sc, gyoto.core.Scenery)
        TestPatternDisk.sc = copy.copy(sc)

    # @unittest.skip("demonstrating skipping")
    def test_fio_PatternDisk1_simple(self):
        # simple save fits
        # print(TestPatternDisk.pd)
        print("========= FISRT CASE simple save fits")
        TestPatternDisk.pd.fitsWrite("!check-patterndisk1.fits.gz")
        print("fitswrite ok")
        # simple Save Scenery
        print("simple save scenery")
        gyoto.core.Factory(TestPatternDisk.sc).write("check-patterndisk1.xml")
        print("factory write ok")
        # simple Read Scenery
        gyoto.core.Factory("check-patterndisk1.xml").scenery()
        print("factory scenery read ok")
        os.unlink("check-patterndisk1.fits.gz")
        os.unlink("check-patterndisk1.xml")

    # @unittest.skip("demonstrating skipping")
    def test_fio_PatternDisk2_prefix(self):
        # Save fits same directory
        print("\n========= SECOND CASE save fits same dir with prefix")
        # si pd fitswrite and save factory should update fillproperty filename
        # order is important
        TestPatternDisk.pd.fitsWrite("!check-patterndisk2.fits.gz",
                                     GYOTO_ARTIFACTS_DIR)
        # TestPatternDisk.pd.fitsWrite("/home/brule/github_jb/Gyoto/python/tests/artifacts/checkpatterndisk2.fits.gz")
        # TestPatternDisk.pd.fitsWrite("!uu.fits.gz")
        print("fitswrite ok")
        # Save Scenery same directory
        print("save scenery fits xml same directory")
        gyoto.core.Factory(TestPatternDisk.sc).write(
            GYOTO_ARTIFACTS_DIR + "check-patterndisk2.xml")
#        gyoto.core.Factory(sc).write("check-patterndisk.xml")
        # pd.fitsWrite("!" + GYOTO_ARTIACTS_DIR + "check-patterndisk2.fits.gz")

        print("factory write ok")
        # Read Scenery same directory
        sc2 = gyoto.core.Factory(GYOTO_ARTIFACTS_DIR
                                 + "check-patterndisk2.xml").scenery()
        print("factory scenery read ok")
        # Check
        # Compare Sceneries
        self.assertEqual(sc2.screen().dMax(), self.sc.screen().dMax(),
                         "dmax was not conserved when RW XML file")
        self.assertEqual(sc2.tMin(), self.sc.tMin(),
                         "tmin was not conserved when RW XML file")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk2.fits.gz")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk2.xml")

    # @unittest.skip("demonstrating skipping")
    def test_fio_PatternDisk3_different_path(self):

        # Save fits different path
        print("========= THIRD CASE save scenery fits xml different directory")
        TestPatternDisk.pd.fitsWrite("!../fits/check-patterndisk3.fits.gz",
                                     GYOTO_XML_DIR)
        print("fitswrite ok")
        # Save Scenery same directory
        print("save scenery fits xml same directory")
        gyoto.core.Factory(TestPatternDisk.sc).write(
            GYOTO_XML_DIR + "check-patterndisk3.xml")

        # pd.fitsWrite("!" + GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        # pd.fitsWrite("check-patterndisk.fits.gz", "LALLAL")
        print("factory write ok")
        # Read Scenery
        gyoto.core.Factory(GYOTO_XML_DIR
                           + "check-patterndisk3.xml").scenery()
        print("factory scenery read ok")
        os.unlink(GYOTO_XML_DIR + "../fits/check-patterndisk3.fits.gz")
        os.unlink(GYOTO_XML_DIR + "check-patterndisk3.xml")

    # @unittest.skip("demonstrating skipping")
    def PatternDisk_zzz(self):
        # Save Scenery different path
        print("========= FOURTH CASE save scenery fits xml diff directory")
        TestPatternDisk.pd.fitsWrite("!check-patterndisk.fits.gz")
        print("fitswrite ok")
        gyoto.core.Factory(self.sc).write(GYOTO_ARTIFACTS_DIR +
                                          "check-patterndisk.xml")
        print("factory write ok")
        # Read Scenery
        gyoto.core.Factory(GYOTO_ARTIFACTS_DIR +
                           "check-patterndisk.xml").scenery()
        print("factory scenery read ok")

        # Delete temporary files
        os.unlink("check-patterndisk.fits.gz")
        os.unlink(GYOTO_ARTIFACTS_DIR + "check-patterndisk.xml")

    @unittest.skip("demonstrating skipping")
    def test_PatternDisk_restore(self):
        TestPatternDisk.pd.fitsWrite("!check-patterndisk3.fits.gz",
                                     GYOTO_ARTIFACTS_DIR)
        print("fitswrite ok")
        # Save Scenery same directory
        print("save scenery fits xml same directory")
        gyoto.core.Factory(TestPatternDisk.sc).write(
            GYOTO_ARTIFACTS_DIR + "check-patterndisk3.xml")

        # pd.fitsWrite("!" + GYOTO_ARTIFACTS_DIR + "check-patterndisk.fits.gz")
        # pd.fitsWrite("check-patterndisk.fits.gz", "LALLAL")
        print("factory write ok")
        # Read Scenery
        scene = gyoto.core.Factory(GYOTO_ARTIFACTS_DIR
                                   + "check-patterndisk3.xml").scenery()
        print("factory scenery read ok")
        # print(f"the scene is\n {scene}")
        # Compare PatternDisks TestPatternDisk.pd scene.pd
        # TODO What is the best way to retrieve the astrobj ??
        # get pd2 from scene
        # pd3 = scene.astrobj()
        # print(f"{type(pd3)=}")
        # print(f"the astrobj is ===== \n {pd3}")
        pd2 = gyoto.std.PatternDisk(scene.astrobj())
        # print(f"{type(pd2)=}")
        # print(f"the astrobj is ===== \n {pd2}")
        # pd4 = gyoto.std.PatternDisk(gyoto.core.Factory(
        #     GYOTO_ARTIFACTS_DIR + "check-patterndisk3.xml").astrobj())
        # print(f"{type(pd4)=}")
        # print(f"the astrobj is ===== \n {pd4}")

        # compare shape
        # pgridshape2 = gyoto.core.array_size_t(3)
        # TODO IMPOSSIBLE pd2 is still an astrobj
        # pd2.getIntensityNaxes(pgridshape2)
        gridshape2 = np.asarray((1, 3, 11), np.uint64)
        pgridshape2 = gyoto.core.array_size_t.fromnumpy1(gridshape2)

        pd2.getIntensityNaxes(pgridshape2)
        # for k in range(3):
        #    assert pgridshape2[k] == self.pgridshape[k], "grid shape changed"
        np.testing.assert_allclose(gridshape2, TestPatternDisk.gridshape,
                                   rtol=1e-07, atol=0)
        # equal_nan=True, err_msg='', verbose=True, *, strict=False)
        print(f"{gridshape2[2]=}")
        print(f"{TestPatternDisk.gridshape[2]=}")
        # compare intensity
        # intensity2 = np.zeros(gridshape2)
        # pintensity2 = gyoto.core.array_double.fromnumpy3(intensity2)
        # print(f"====== {type(intensity2[0, 0, 0])=}")
        print(f"====== {type(TestPatternDisk.intensity[0, 0, 0])=}")
        # intensity2 = gyoto.core.array_double.frompointer(pd2.getIntensity())
        # print(f"====== {type(intensity2[0, 0, 0])=}")
        # np.testing.assert_allclose(intensity2, TestPatternDisk.intensity,
        #                           rtol=1e-07, atol=0)
        # intensity3 = pd2.getIntensity()
        # print(f"====== {type(intensity3)=}")
        # TODO find new way print(f"====== {type(intensity3[0, 0, 0])=}")
        bufsize = self.gridshape.prod()
        buf = gyoto.core.array_double.frompointer(pd2.getIntensity())
        print(f"{type(buf)=}")
        print(f"{type(self.pintensity)=}")
        for k in range(bufsize):
            # np.testing.assert_almost_equal(buf[k], pintensity[k])
            assert buf[k] == self.pintensity[k], "Intensity changed"
            # print(f"buf {buf[k]}")
            # print(f"{self.pintensity[k]}")

        # compare opacity
        # opacity2 = np.zeros(gridshape2)
        # pacity2 = gyoto.core.array_double.fromnumpy3(opacity2)
        pd2.opacity()
        buf = gyoto.core.array_double.frompointer(pd2.opacity())
        for k in range(bufsize):
            assert buf[k] == self.popacity[k], "Opacity changed"
            # print(f"buf {buf[k]}")
            # print(f"{self.popacity[k]}")

#                self.assertTrue(False)
        # np.testing.assert_allclose(pgridshape2, TestPatternDisk.pgridshape,
        #                           rtol=1e-07, atol=0)

        # numpy testing
        # testing.assert_allclose(actual, desired, rtol=1e-07, atol=0,
        # equal_nan=True, err_msg='', verbose=True, *, strict=False)

    @unittest.skip("demonstrating skipping")
    def test_PatternDisk_raytrace(self):
        print(f"{type(TestPatternDisk)=}")
        # print(f"{type(self.sc)=}")
        # TODO why print(f"{type(TestPatternDisk.sc)=}")
        screen = self.create_screen()
        # sc = self.create_scenery()
        # Ray-trace
        ii = gyoto.core.Range(1, screen.resolution(), 1)
        jj = gyoto.core.Range(1, screen.resolution(), 1)
        grid = gyoto.core.Grid(ii, jj)
        aop = gyoto.core.AstrobjProperties()
        frame = np.zeros((screen.resolution(), screen.resolution()))
        pframe = gyoto.core.array_double.fromnumpy2(frame)
        aop.intensity = pframe
        TestPatternDisk.sc.rayTrace(grid, aop)
        plt.figure()
        plt.imshow(frame, origin='lower')
        # plt.savefig(frame)
        file_output = PdfPages(GYOTO_ARTIFACTS_DIR + "check-patterndisk.pdf")
        file_output.savefig()
        plt.close()
        file_output.close()
        # plt.imshow(frame, origin='lower')
        # plt.show()
        print("PatternDisk raytrace done")

    @unittest.expectedFailure
    def test_create_obj_assert(self):
        self.assertTrue(False)
#
#    def test_create_obj_assertTrue(self):
#        assert True


if __name__ == '__main__':
    # not good enough
    # unittest.TestLoader.sortTestMethodsUsing = None
    # unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1
    unittest.main()
