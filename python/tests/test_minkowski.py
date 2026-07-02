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
import gyoto.std
import numpy as np
import gyoto.metric
import gyoto.astrobj
import gyoto.spectrum
import gyoto.spectrometer
# import std
# import inspect
# import matplotlib.pyplot as plt
# import helpers as helpers
# from helpers import helpers as hlpr
# import std as test_std
gyoto.core.requirePlugin('stdplug')

# test_metric = test_std.TestStdMetric()
# print(type(test_metric))
# gg = gyoto.core.Metric("Minkowski")
# pos = test_metric.pos(gg)
# print(f"{pos=}")


# from yorick
# include "check-helpers.i"


# create object
# create metric
# create parameters
# associate metric /param to the object
# create scenery

# minkowski = metrique plate tdot=1 le reste a zero

# include "check-helpers.i"
# GYOTO_EXAMPLES_DIR = os.path.join("./", "../../doc/examples/")

# There is no specific Yorick interface for the Minkowski metric.
# The only limitation is that is is not possible to retrieve the kind
# of coordinate system in use.


# class TestMinkowski(unittest.TestCase):
class TestMinkowski(unittest.TestCase):
    def test_Minkowski(self):
        print("Checking gyoto Minkowski")
        gg = gyoto.std.Minkowski()
        self.assertIsInstance(gg, gyoto.std.Minkowski)

    # @unittest.skip("demonstrating skipping")
    def test_Minkowski_cartesian(self):

        print("Minkowski metric in cartesian coordinates")

        # positions = np.array([[0, 10., 12., 5.],
        #                       [0, 5., 2., 7.],
        #                       [0, -10., 0., 50.],
        #                       [0, 0., 0., 10000.]])

        print("creating Minkowski metric")
        gg = gyoto.std.Minkowski()

        # print(gg)

        # coef = np.zeros((4, 4))
        # for i in range(4):
        #    hlpr.test_gmunu(hlpr, gg, positions[i])
        # gyoto.metric.check_gmunu(gg, positions)
        # gyoto.metric.check_christoffel(gg, positions)

        print("creating Star in this metric")
        st = gyoto.std.Star()
        st.metric(gg)
        # st.set("DeltaMaxOverR", np.inf)
        # attention avec pos = (0., 0., 0., 0.)
        pos = (0., 1000., 0., 0.)
        vel = (0., 0., 0.)
        # st.setInitCoord(np.append(np.append(pos, 1.), vel))
        st.setInitCoord(pos, vel)
        gg.set("DeltaMaxOverR", "DBL_MAX")
        print("done")
        print(st)
        print("integrating geodesic")
        # 1000. la date a depasser
        # delta le pas
        st.xFill(1000.)
        print("done")
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        print(f"produce {n=} elements")
        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        tdot = np.ndarray(n)
        xdot = np.ndarray(n)
        ydot = np.ndarray(n)
        zdot = np.ndarray(n)

        # récupérer le tableau des dates
        st.get_t(t)
        self.assertTrue(max(t) > 1000 and min(t) < 1000)
        # récupérer les 3 autres coordonnées
        st.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)
        print("checking results")
        print(f"{t.shape=}")
        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")
        print(f"{tdot=}")
        print(f"{xdot=}")
        print(f"{ydot=}")
        print(f"{zdot=}")

        data = np.column_stack((t, x, y, z, tdot, xdot, ydot, zdot))
        print(f"{data.shape=}")
        print(f"{data=}")
        print("=================")

        # print(f"integration produced {d[1]} rows")
        # TODO JB assert a faire
        # assert de numpy.testing et python
        # https://stackoverflow.com/questions/3302949/best-way-to-assert-for-numpy-array-equality

        # if (!(allof(data(,2:)==([0., 0, 0, 1., 0, 0, 0](-:1:d(2), )))))
        # assert np.allclose(t, np.reshape(
        #    np.repeat([0., 0, 0, 1., 0, 0, 0], d[0]), (-1, d[0])))

        print("done")

    def test_Minkowski_cartesian_other(self):
        print("creating Minkowski metric")
        gg = gyoto.std.Minkowski()

        print("checking another star")
        pos = (0., 4., 2., 6.)
        vel = (0.5, 0.2, 0.4)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord(pos, vel)
        st.xFill(1000.)
        n = st.get_nelements()
        print(f"{n=}")

        t = np.ndarray(n)
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        tdot = np.ndarray(n)
        xdot = np.ndarray(n)
        ydot = np.ndarray(n)
        zdot = np.ndarray(n)
        st.get_t(t)

        st.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)
        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")
        print(f"{tdot=}")
        print(f"{xdot=}")
        print(f"{ydot=}")
        print(f"{zdot=}")

        data = np.column_stack((t, x, y, z))
        print(f"{data.shape=}")
        maxerr = (np.max(
            np.abs(minmax(
                data[:, 1:4]
                - np.expand_dims(data[:, 0], 1)
                * vel[:] - pos[1:4]))))
        if (maxerr > 1e-10):
            print("cartesian other")
            print("error integration produced wrong results")
        print("done\n")

    def test_Minkowski_cartesian_photon(self):

        print("creating Minkowski metric")
        gg = gyoto.std.Minkowski()
        print("checking a photon")
        pos = (0., 4., 2., 6.)
        vel = (0.5, 0.2, 0.4)
        photon = gyoto.core.Photon()
        photon.metric(gg)
        # use nullifyCoord to compute dt/dtau
        coord = np.concatenate((pos, (0,), vel))
        gg.nullifyCoord(coord)
        print(coord)
        photon.initCoord(coord)
        print(photon.initCoord())
        photon.xFill(10.)
        n = photon.get_nelements()
        print(f"{n=}")

        t = np.ndarray(n)
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        tdot = np.ndarray(n)
        xdot = np.ndarray(n)
        ydot = np.ndarray(n)
        zdot = np.ndarray(n)

        photon.get_t(t)
        photon.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)
        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")
        print(f"{tdot=}")
        print(f"{xdot=}")
        print(f"{ydot=}")
        print(f"{zdot=}")

        data = np.column_stack((t, x, y, z, tdot, xdot, ydot, zdot))
        print(f"{data.shape=}")
        print(f"{data=}")
        print("=================")
        nrows = data.shape[0]
        norm = np.zeros(nrows)
        for i in range(nrows):
            norm[i] = gg.ScalarProd(data[i, 0:4], data[i, 4:8], data[i, 4:8])
        if (max(norm) > 1e-10):
            print("error: norm was not conserved")

        print(data.shape[0])
        maxerr = (np.max(
            np.abs(
                minmax(data[:, 1:4] -
                       np.expand_dims(data[:, 0], 1) * np.expand_dims(vel, 0)
                       / np.expand_dims(data[:, 4], 1)
                       - np.expand_dims(pos[1:], 0)))))
        if (maxerr > 1e-10):
            print("cartesian photon")
            print("error integration produced wrong results")

    def test_Minkowski_cartesian_star_2(self):
        pos = (0., 4., 2., 6.)
        vel = (0.5, 0.2, 0.4)

        gg = gyoto.std.Minkowski()
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord(pos, vel)
        st.xFill(1000.)
        n = st.get_nelements()
        print(f"{n=}")

        t = np.zeros(n)
        x = np.zeros(n)
        y = np.zeros(n)
        z = np.zeros(n)
        tdot = np.ndarray(n)
        xdot = np.ndarray(n)
        ydot = np.ndarray(n)
        zdot = np.ndarray(n)
        st.get_t(t)

        st.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)
        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")
        # data = np.concatenate((t, x, y, z))
        # print(f"{data.shape=}")
        # print(f"(integration produced {len(data)} rows)...")
        data = np.column_stack((t, x, y, z, tdot, xdot, ydot, zdot))
        print(f"{data.shape=}")
        print(f"{data=}")
        print("=================")
        nrows = data.shape[0]
        norm = np.zeros(nrows)
        for i in range(nrows):
            norm[i] = gg.ScalarProd(data[i, 0:4], data[i, 4:8], data[i, 4:8])
        if (max(norm) > 1e-10):
            print("error: norm was not conserved")

        print(data.shape[0])

        # don't work with Photon
        # st.setInitCoord(pos, vel)

        nrows = data.shape[0]
        norm = np.zeros(nrows)
        for i in range(nrows):
            norm[i] = gg.ScalarProd(data[i, 0:4], data[i, 4:8], data[i, 4:8])
        if (max(norm) > 1e-10):
            print("error: norm was not conserved")

        maxerr = (np.max(
            np.abs(
                minmax(data[:, 1:4] -
                       np.expand_dims(data[:, 0], 1) * np.expand_dims(vel, 0)
                       / np.expand_dims(data[:, 4], 1)
                       - np.expand_dims(pos[1:], 0)))))
        if (maxerr > 1e-10):
            print("cartesian star 2")
            print("error integration produced wrong results")

        # maxerr = (np.max(
        #    np.abs(
        #        minmax(data[:, 1:3] -
        #               np.expand_dims(data[:, 0], 1) * np.expand_dims(vel, 1)
        #               / np.expand_dims(data[:, 4], 1)
        #               - np.reshape(np.repeat(pos, 2), (-1, 4))))))
        # if (maxerr > 1e-10):
        #    print("error integration produced wrong results")
        print("done")

    def test_Minkowski_spherical_coordinates(self):
        print("Minkowski metric in spherical coordinates")
        print("creating Minkowski metric")
        gg = gyoto.std.Minkowski()

        print("changing coordinate system")
        gg.spherical(True)
        print("done\n")
        # TODO
        # positions = [[0, 10., np.pi / 2., 0.],
        #             [100., 10., np.pi / 4., 2.],
        #             [1000., 100., 1., 1.]]

        # for i in range(2):
        #    hlpr.test_gmunu(hlpr, gg, positions[i])
        # gyoto.metric.check_gmunu(gg, positions)
        # gyoto.metric.check_christoffel(gg, positions)
        # TODO voir implementation python
        # hlpr.check_gmunu(gg, positions)
        # hlpr.check_christoffels(gg, positions)

    def test_Minkowski_motionless_star(self):
        gg = gyoto.std.Minkowski()
        gg.spherical(True)
        print("checking motionless star")
        pos = (0., 4., 2., 6.)
        vel = (0., 0., 0.)
        st = gyoto.std.Star()
        st.metric(gg)
        print(st)
        # call to std.py test
        # std_test = std.TestMinkowski()
        # t, x, y, z, tdot, xdot, ydot, zdot
        # = std_test._compute_orbit(gg, st, pos, np.concatenate(((1,), vel)))
        # use nullifyCoord to compute dt/dtau if phoon
        # else in the general case use SysPrimeToTdot to compute dt/dtau
        # see std.py
        coord = np.concatenate((pos, (1,), vel))
        st.initCoord(coord)
        print(st.initCoord())
        st.xFill(10.)
        n = st.get_nelements()
        print(f"{n=}")

        t = np.zeros(n)
        x = np.zeros(n)
        y = np.zeros(n)
        z = np.zeros(n)
        tdot = np.zeros(n)
        xdot = np.zeros(n)
        ydot = np.zeros(n)
        zdot = np.zeros(n)

        st.get_t(t)
        st.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)
        data = np.column_stack((t, x, y, z, tdot, xdot, ydot, zdot))
        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")
        print(f"{tdot=}")
        print(f"{xdot=}")
        print(f"{ydot=}")
        print(f"{zdot=}")

        print(f"{data=}")
        print(f"{data.shape=}")
        # TODO pas la meme shape que yorick
        print(f"(integration produced {data.shape[0]} rows)...")
        # yorick line
        # if (!(allof(data(,2:)==(_(pos(2:),[1.],vel)(-:1:d(2), ))))):

        # tmp = (pos[2:], [1.], vel)[-:1:d[2], ]
        # if (data[:, 1:] == np.reshape(np.repeat([0., 0, 0, 1., 0, 0, 0], 3),
        #                             (-1, 3))).all:
        print(f"{(pos[1:], (1,), vel)=}")
        # data_ref = np.reshape(np.repeat(np.concatenate((pos[1:], (1,), vel)),
        #                                data.shape[1]), (-1, 3))
        # * np.arange(1, data.shape[1] + 1)[:, np.newaxis]
        # np.expand_dims(data_ref, axis=1)
        # np.repeat(u , 8, 1)
        data_ref = np.repeat(np.expand_dims(
            np.concatenate((pos[1:], (1,), vel)), axis=0), 8, 0)
        print(f"{data_ref.shape=}")
        print(f"{data_ref=}")
        np.testing.assert_almost_equal(data_ref, data[:, 1:])
        # if (data[:, 1:] != data_ref):
        #    print("error integration produced wrong results")
        print("done")

    def test_Minkowski_moving_star(self):
        gg = gyoto.std.Minkowski()
        # gg.spherical(False)

        print("checking moving star")
        pos = [0., 10.791, np.pi / 2., 0]
        vel = [0., 0., 0.016664]
        # st = Star(metric=gg, initcoord=pos, vel)
        st = gyoto.std.Star()
        st.metric(gg)
        # coord = np.concatenate((pos, (0,), vel))
        # TODO pkoi pas la ?
        # gg.nullifyCoord(coord)
        coord = np.concatenate((pos, (1,), vel))
        st.initCoord(coord)
        print(st.initCoord())
        st.adaptive(True)
        st.delta(0.1)
        print(st)
        st.xFill(10.)
        n = st.get_nelements()
        print(f"{n=}")

        # data = st.getCoord()
        # d = data.shape
        t = np.ndarray(n)
        x = np.ndarray(n)
        # px = gyoto.core.array_double.fromnumpy1(x)
        y = np.ndarray(n)
        # py = gyoto.core.array_double.fromnumpy1(y)
        z = np.ndarray(n)
        # pz = gyoto.core.array_double.fromnumpy1(z)

        tdot = np.ndarray(n)
        xdot = np.ndarray(n)
        ydot = np.ndarray(n)
        zdot = np.ndarray(n)
        # index = np.ndarray(n, np.uint64)
        # pindex = gyoto.core.array_size_t.fromnumpy1(index)

        # grid = np.zeros(8)
        # pgrid = gyoto.core.array_double.fromnumpy1(grid)

        # txyz=st(get_cartesian=dates)
        # récupérer le tableau des dates
        st.get_t(t)
        # récupérer les 3 autres coordonnées
        # st.get_xyz(x, y, z)
        # data = st.getCartesianPos(pindex, pgrid)
        # data = st.getCartesianPos(t, x, y, z)
        # st.getCartesian(t, x, y, z)
        st.getCoord(t, x, y, z, tdot, xdot, ydot, zdot)

        print(f"{t=}")
        print(f"{x=}")
        print(f"{y=}")
        print(f"{z=}")

        # data2 = np.concatenate((t, x, y, z))
        # data = st.getCoord(t, x, y, z)

        data = np.column_stack((t, x, y, z, tdot, xdot, ydot, zdot))
        # data = np.vstack((t, x, y, z, tdot, xdot, ydot, zdot))
        d = data.shape
        print(f"{d=}")
        print(f"{data=}")
        print(f"integration produced {d[0]} rows)...")
        # if (!(allof(data(,2:)==(_(pos(2:),[1.],vel)(-:1:d(2), )))))
        data_ref = np.repeat(np.expand_dims(
            np.concatenate((pos[1:], (1,), vel)), axis=0), 5, 0)
        print(f"{data_ref.shape=}")
        print(f"{data_ref=}")
        # unequal_pos = np.where(data[:, 1:] != data_ref)
        # other = np.count_nonzero(data[:, 1:] != data_ref)
        # print(f"{unequal_pos=}")
        # print(f"{other=}")
        # pas possible ca BOUGE
        # np.testing.assert_allclose(data[:, 1:], data_ref)
        # np.testing.assert_almost_equal(data[:, 1:], data_ref, decimal=7)
        # np.testing.assert_array_almost_equal_nulp(data[:, 1:], data_ref)

        # print("error integration produced wrong results")
        print("done")
        print("end Minkowski metric")


def minmax(data):
    data = data.flatten()
    max = min = data[0]
    for i in range(1, len(data), 2):
        try:
            a, b = data[i:i + 2]
        except ValueError:
            a = b = data[i]
        if b > a:
            a, b = b, a
        if a > max:
            max = a
        if b < min:
            min = b
    return [min, max]


if __name__ == '__main__':
    unittest.main()
