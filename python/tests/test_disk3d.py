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
from pathlib import Path
import unittest
import gyoto.core
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import inspect
# import matplotlib.pyplot as plt

GYOTO_EXAMPLES_DIR = "../../doc/examples/"
GYOTO_ARTIFACTS_DIR = "artifacts/"


class TestDisk3D(unittest.TestCase):
    def test_Disk3D(self):
        # gyoto.core.debug(1)
        gyoto.core.verbose(10)
        print(f"path {sys.argv[0]=}")
        dirname, filename = os.path.split(os.path.abspath(__file__))
        print(f"running from {dirname}")
        print(f"file is {filename}")
        # using pathlib
        print("using pathlib")
        path = Path(__file__)
        print(path.parts)
        # emiss
        emissquant_shape = np.asarray((1, 2, 10, 10), np.uint64)
        pemissquant_shape = gyoto.core.array_size_t.fromnumpy1(
            emissquant_shape)
        emissquant = np.zeros(emissquant_shape, np.float64)
        emissquant[:, 0, :, 0:2] = 100.
        emissquant[:, 1, :, 3:9] = 100.
        pemissquant = gyoto.core.array_double.fromnumpy4(emissquant)
        # velocity
        velocity_shape = np.asarray((2, 10, 10), np.uint64)
        pvelocity_shape = gyoto.core.array_size_t.fromnumpy1(velocity_shape)
        velocity = np.ones(velocity_shape)
        pvelocity = gyoto.core.array_double.fromnumpy3(velocity)
        # metric
        metric = gyoto.std.KerrBL()
        metric.set("Mass", 4e6 * gyoto.core.GYOTO_SUN_MASS)
        print("Creating Disk3D...")
        pd = gyoto.std.Disk3D()
        pd.copyEmissquant(pemissquant, pemissquant_shape)
        pd.copyVelocity(pvelocity, pvelocity_shape)
        pd.rin(3)
        pd.rout(28)
        pd.zmin(1.)
        pd.zmax(10.)
        pd.phimin(0.)
        pd.phimax(2. * np.pi)
        pd.repeatPhi(8)
        pd.metric(metric)

        print("Printing Disk3D:")
        screen = gyoto.core.Screen()
        screen.metric(metric)
        screen.resolution(64)
        screen.time(1000. * metric.unitLength() / gyoto.core.GYOTO_C)
        screen.distance(100. * metric.unitLength())
        screen.set("FieldOfView", 30. / 100.)
        screen.inclination(110. / 180. * np.pi)
        screen.set("PALN", np.pi)
        print("Attaching Disk3D to scenery...")
        sc = gyoto.core.Scenery()
        sc.metric(metric)
        sc.screen(screen)
        sc.astrobj(pd)
        print("Saving data to fits file...")

        print(f"the scene is\n {sc}")
        # Save Scenery
        pd.fitsWrite("!check-disk3d.fits.gz")
        print("Saving scenery to XML file...")
        gyoto.core.Factory(sc).write("check-disk3d.xml")
        print("Reading back scenery...")
        sc2 = gyoto.core.Factory("check-disk3d.xml").scenery()
        # sc2 = gyoto.core.Scenery("check-disk3d.xml")
        print("Removing temporary files...")
        os.remove("check-disk3d.xml")
        os.remove("check-disk3d.fits.gz")
        print("Cloning...")
        sc2 = sc.clone()

        print(f"the scene is\n {sc2}")
        # compare the two cube emissquant values
        print("Getting Disk3D...")
        pd2 = gyoto.std.Disk3D(sc2.astrobj())
        print(f"{type(pd2)=}")
        print("Comparing emissquant array...")
        # a = pd2.getEmissquant()
        # b = gyoto.core.array_double.frompointer(a)
        naxes = np.zeros(4, np.uint64)
        pnaxes = gyoto.core.array_size_t.fromnumpy1(naxes)
        pd2.getEmissquantNaxes(pnaxes)
        print(f"{type(pd2)=}")
        print(f"{pnaxes=}")
        print(f"{naxes=}")
        buf_emiss_size = naxes.prod()
        print(f"{buf_emiss_size=}")
        print(f"buf size {naxes.prod()=}")
        emissquant2 = np.zeros(naxes)
        # pemissquant2 = gyoto.core.array_size_t.fromnumpy4(emissquant2)
        # pemissquant2 = gyoto.core.array_double.fromnumpy4(emissquant2)
        # pd2.copyEmissquant(pemissquant2, pnaxes)
        print(f"{emissquant2[:, 0, :, 0:2]=}")

        # TODO A VOIR CTYPE
        # bufsize = naxes.prod()
        # buf2 = gyoto.core.array_double.frompointer(emissquant2)
        pd2.getEmissquant()
        print(f"{type(pd2)=}")
        print(f"{pd2.__dict__=}")
        print(f"{pd2.__dict__["this"]=}")
        vars(pd2)
        buf_emiss = gyoto.core.array_double.frompointer(pd2.getEmissquant())
        print(f"{type(buf_emiss)=}")
        # print(f"{buf.size()=}")
        vars(buf_emiss)
        print(f"{buf_emiss.__getitem__=}")
        # print(f"{help(buf)=}")
        # array = np.frombuffer(buf)
        # array = np.frombuffer(pd2.getEmissquant())
        # print(f"{type(array)=}")
        # print(f"{array[:, 0, :, 0:2]=}")
        # for k in range(bufsize):
        #    print(f"{buf[k]=}")
        # np.testing.assert_almost_equal(buf[k], pintensity[k])
        #    assert buf[k] == emissquant[k], "Emissquant changed"
        # print(f"{buf[0]=}")
        # print(f"{pemissquant[0]=}")

        # print(f"{buf[100]=}")
        # print(f"{pemissquant[100]=}")
        for k in range(buf_emiss_size):
            assert buf_emiss[k] == pemissquant[k], "Emissquant changed"
            # print(f"{buf[k]=}")
            # print(f"{pemissquant[k]=}")

        # print(f"{emissquant[:, 0, :, 0:2]=}")
        # print(f"{emissquant2[:, 0, :, 0:2]=}")
        # if any(emissquant != pd2.copyEmissquant(pemissquant2, pnaxes)):
        #    print("CHECK FAILED")
        #    print(" done.")
        #    print("Comparing velocity array...")
        # if any(velocity != pd2.copyVelocity()):
        #    print("CHECK FAILED")
        #    print(" done.")

        # velocity

        buf_velocity_size = velocity_shape.prod()
        # velocity = np.ones((2, 10, 10), np.uint64)
        # pvelocity = gyoto.core.array_double.fromnumpy3(velocity)
        # velocity_shape = velocity.shape()
        # pvelocity_shape = gyoto.core.array_size_t.fromnumpy1(velocity_shape)
        buf_velocity = gyoto.core.array_double.frompointer(pd2.getVelocity())
        for k in range(buf_velocity_size):
            assert buf_velocity[k] == pvelocity[k], "Velocity changed"
            print(f"{buf_velocity[k]=}")
            print(f"{pvelocity[k]=}")
        # pas possible avec type array_double
        # np.testing.assert_array_almost_equal(pvelocity, buf_velocity)


if __name__ == '__main__':
    unittest.main()
