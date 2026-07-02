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
import unittest
import gyoto.core
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import inspect
# import matplotlib.pyplot as plt

from tests.helpers import helpers

gyoto.core.requirePlugin('stdplug')

# from yorick
# include "check-helpers.i"


# create object
# create metric
# create parameters
# associate metric /param to the object
# create scenery

GYOTO_EXAMPLES_DIR = "../../doc/examples/"


class TestKerrKS(unittest.TestCase):
    hlpr = helpers()

    def construct_kerrks(self):
        print("Checking gyoto_KerrKS:")
        gg = gyoto.std.KerrKS()
        self.assertIsInstance(gg, gyoto.std.KerrKS)

    def test_setter_getter_kerrks(self):
        print("Checking setter getter gyoto_KerrKS:")
        gg = gyoto.std.KerrKS()
        gg.set("Spin", 0.)
        self.assertEqual(gg.get("Spin"), 0.)

    def test_KerrKS(self):
        print("KerrKS metric Kerr in Kerr-Schild coordinates")
        print("creating KerrKS metric")
        gg = gyoto.std.KerrKS()
        gg.spin(0.)
        print("done")

        positions = ((0, 10., 12., 5.),
                     (0, 5., 2., 7.),
                     (0, -10., 0., 50.),
                     (0, 0., 0., 10000.))

        # check_gmunu, gg, positions;
        # check_gmunu_up, gg, positions;

        print("checking dk")
        pos = [0, 10., 12., 5.]
        dk1 = self.hlpr.dkfunc(gg, pos)
        dk3 = self.hlpr.dknum(gg, pos)
        np.testing.assert_array_almost_equal(dk1, dk3)
        # if (max(abs(dk1 - dk3)) > 1e-5):
        #   print("error dk is wrong")
        # print("done")

        print("checking df")
        pos = np.array([0, 10., 12., 5.])
        df1 = self.hlpr.dffunc(gg, pos)
        df3 = self.hlpr.dfnum(gg, pos)
        np.testing.assert_array_almost_equal(df1, df3)
        # if (max(abs(df1 - df3)) > 1e-6):
        #     print("error df is wrong")
        # print("done")

        print("checking jacobian")
        # check_jacobian, gg, positions;
        # self.hlpr.check_jacobian(gg, pos)
        a = gg.jacobian(pos)
        b = gyoto.metric.jacobian_numerical(gg, pos, epsilon=1e-06)
        print(a)
        print(f"{type(a)=}")
        print(b)
        print(f"{type(b)=}")

        np.testing.assert_array_almost_equal(a, b)
        print("checking christoffel")
        # check_christoffels, gg, positions;
        pos = (0, 10., 12., 5.)
        # TODO renvoi None
        print(f"{type(gg)=}")
        print(f"{gg.Spin=}")
        try:
            gyoto.metric.check_christoffel(gg, positions, epsilon=1e-06)
        except AssertionError as e:
            self.fail(e.__str__())
        b = gyoto.metric.christoffel_numerical(gg, pos, epsilon=1e-06)
        # np.testing.assert_array_almost_equal(a, b)
        print(a)
        print(f"{type(a)=}")
        print(b)
        print(f"{type(b)=}")

        print("KerrKS metric Kerr in Kerr-Schild coordinates")


if __name__ == '__main__':
    unittest.main()
