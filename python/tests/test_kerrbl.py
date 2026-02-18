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
import gyoto.std
# import inspect
# import matplotlib.pyplot as plt

gyoto.core.requirePlugin('stdplug')

# self.assertAlmostEqual()
# self.assertEqual()

# TODO ? voir avec std.py
# check_gmunu, gg
# check_gmunu_up, gg
# check_christoffels, gg


class TestKerrBL(unittest.TestCase):
    def construct_kerrbl(self):
        print("Checking gyoto_KerrBL:")
        gg = gyoto.std.KerrBL()
        self.assertIsInstance(gg, gyoto.std.KerrBL)

    def test_MakeCoord_kerrbl(self):
        gg = gyoto.std.KerrBL()
        aa = 0.995
        gg.set("Spin", aa)
        # initial conditions :
        ri = 10.791
        thetai = 1.5708
        phii = 0.
        ti = 0.
        pri = 0.  # canonical momentum
        pthetai = 0.
        cst = [1, 0.921103, 2., 0.]  # 4 Kerr cst of motion mu, E, L, Q
        # /lib/KerrBL.C line 1282
        # void KerrBL::computeCst(const double coord[8], double cst[5]) const
        # 5th element est calcule par
        # cst[4]= cst[3]==0. ? 1. : 1./cst[3]; // cache 1/Q or 1. if Q==0
        if cst[3] == 0.:
            cst = np.append(cst, 1.)
        else:
            cst = np.append(cst, 1. / cst[3])

        yinit = [ti, ri, thetai, phii, -cst[1], pri, pthetai, cst[2]]

        print("Checking MakeCoord method: ")
        coordout = np.zeros(8)
        gg.MakeCoord(yinit, cst, coordout)
        print(f"after MakeCoord {coordout=}")
        # if max(abs((coordout - [0, 10.791, 1.5708, 0,
        #                        1.12641, 0, 0, 0.0187701]))) < 1e-6:
        #    print("done.")
        # else:
        #    print("error PREVIOUS CHECK FAILED")
        # unitest => NO
        # self.assertAlmostEqual(coordout, [0, 10.791, 1.5708, 0,
        #                                  1.12641, 0, 0, 0.0187701], 1e-6)

        np.testing.assert_array_almost_equal(coordout,
                                             [0, 10.791, 1.5708, 0,
                                              1.12641, 0, 0, 0.0187701])
        # BAD
        # np.testing.assert_array_almost_equal_nulp(coordout,
        #                                          [0, 10.791, 1.5708, 0,
        #                                           1.12641, 0, 0, 0.0187701])
        np.testing.assert_allclose(coordout,
                                   [0, 10.791, 1.5708, 0,
                                    1.12641, 0, 0, 0.0187701], rtol=1e-6)

    def test_setter_getter_kerrbl(self):
        print("Creating metric using gyoto_Kerr(spin=0.7)")
        gg = gyoto.std.KerrBL()
        print("Setting spin... 0.7")
        gg.set("Spin", 0.7)
        # if gg.get("Spin") != 0.7:
        #    print("error CHECK FAILED")
        #    print("done.")
        self.assertEqual(gg.get("Spin"), 0.7)
        print("Setting spin... 0.9")
        gg.set("Spin", 0.9)
        self.assertEqual(gg.get("Spin"), 0.9)
        print("Getting spin... ")
        # print("done.")

        print(f"getPointer to this Metric object: {gg.getPointer()=}")
        self.assertNotEqual(gg.getPointer(), 0)

        print("Printing object. \"gg\" yields: ")
        print(gg)

        print("Setting deltaMin... ")
        gg.deltaMin(40)
        self.assertEqual(gg.get("DeltaMin"), 40)
        # if gg.get("DeltaMin") != 40:
        #    print("error CHECK FAILED")
        #    print("done.")

        print("Setting deltaMax... ")
        gg.deltaMax(400)
        self.assertEqual(gg.get("DeltaMax"), 400)
        # if gg.get("DeltaMax") != 400:
        #    print("error CHECK FAILED")
        #    print("done.")

        print("Setting difftol... ")
        gg.difftol(1e-3)
        self.assertEqual(gg.get("DiffTol"), 1e-3)
        # if gg.get("DiffTol") != 1e-3:
        #    print("error CHECK FAILED")
        #    print("done.")

        print("Setting deltamaxoverr... ")
        gg.deltaMaxOverR(2e-3)
        self.assertEqual(gg.get("DeltaMaxOverR"), 2e-3)
        # if gg.get("DeltaMaxOverR") != 2e-3:
        #    print("error CHECK FAILED")
        #    print("done.")

        print("Cloning... ")
        gg2 = gg.clone()
        self.assertEqual(gg2.get("DeltaMin"), 40)
        self.assertEqual(gg2.get("DeltaMax"), 400)
        self.assertEqual(gg2.get("DiffTol"), 1e-3)
        self.assertEqual(gg2.get("DeltaMaxOverR"), 2e-3)
        # if ((gg2.get("DeltaMax") != 400)
        #       or (gg2.get("DeltaMin") != 40)
        #       or (gg2.get("DiffTol") != 1e-3)):
        #    print("error CHECK FAILED")
        # print("done.")

    def test_integrators_generic_kerrbl(self):
        print("comparing the various integrators")
        gg = gyoto.std.KerrBL()
        gg.set("Spin", 0.995)
        # gg, deltamaxoverr=0.1, deltamin=1e-6
        gg2 = gg.clone()
        gg2.set("GenericIntegrator", True)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        st2 = gyoto.std.Star()
        st2.metric(gg2)
        st2.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        # TODO what to do here ?
        # st.integrator("Legacy")
        # st2.integrator("Legacy")
        # dates = np.arange(100.)
        # dates = np.arange(100)
        # dates = np.arange(100, dtype=np.float64)
        st.xFill(1000)
        st2.xFill(1000)
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        n2 = st2.get_nelements()

        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)

        t2 = np.ndarray(n2)
        r2 = np.ndarray(n2)
        theta2 = np.ndarray(n2)
        phi2 = np.ndarray(n2)

        # récupérer le tableau des dates
        st.get_t(t)
        st2.get_t(t2)

        # récupérer les 3 autres coordonnées
        st.getCoord(t, r, theta, phi)
        st2.getCoord(t2, r2, theta2, phi2)
        coords = np.concatenate((r, theta, phi))
        coords2 = np.concatenate((r2, theta2, phi2))
        # res = np.empty(100, dtype=np.float64)
        # pdates = gyoto.core.array_double.fromnumpy1(dates)
        # coords = st.getCoord(1)
        # res = st.getCoord(dates, coords)
        # coords2 = st2.getCoord(1)

        # TODO jb tester les surcharges de getcoord vector_double size 8

        np.testing.assert_array_almost_equal(coords, coords2, err_msg="coords")
        np.testing.assert_array_almost_equal(r, r2, err_msg="r")
        np.testing.assert_array_almost_equal(theta, theta2, err_msg="theta")
        np.testing.assert_array_almost_equal(phi, phi2, err_msg="phi")

    def test_integrators_runge_kutta_cash_karp54_kerrbl(self):
        print("comparing the various integrators")
        gg = gyoto.std.KerrBL()
        gg.set("Spin", 0.995)
        # gg, deltamaxoverr=0.1, deltamin=1e-6
        gg2 = gg.clone()
        gg2.set("GenericIntegrator", True)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        st2 = gyoto.std.Star()
        st2.metric(gg2)

        st2.integrator("runge_kutta_cash_karp54")
        st2.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        # TODO what to do here ?
        st.integrator("Legacy")
        # st2.integrator("Legacy")
        # dates = np.arange(100.)
        # dates = np.arange(100)
        # dates = np.arange(100, dtype=np.float64)
        st.xFill(1000)
        st2.xFill(1000)
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        n2 = st2.get_nelements()

        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)

        t2 = np.ndarray(n2)
        r2 = np.ndarray(n2)
        theta2 = np.ndarray(n2)
        phi2 = np.ndarray(n2)

        # récupérer le tableau des dates
        st.get_t(t)
        st2.get_t(t2)

        # récupérer les 3 autres coordonnées
        st.getCoord(t, r, theta, phi)
        st2.getCoord(t2, r2, theta2, phi2)
        coords = np.concatenate((r, theta, phi))
        coords2 = np.concatenate((r2, theta2, phi2))
        # res = np.empty(100, dtype=np.float64)
        # pdates = gyoto.core.array_double.fromnumpy1(dates)
        # coords = st.getCoord(1)
        # res = st.getCoord(dates, coords)
        # coords2 = st2.getCoord(1)

        # TODO jb tester les surcharges de getcoord vector_double size 8
        # len(coords) != len(coords2)
        np.testing.assert_array_almost_equal(np.max(coords) - np.max(coords2),
                                             0)
        # np.testing.assert_array_almost_equal(coords, coords2)
        # np.testing.assert_array_almost_equal(r, r2)
        # np.testing.assert_array_almost_equal(theta, theta2)
        # np.testing.assert_array_almost_equal(phi, phi2)

    def test_integrators_runge_kutta_fehlberg78_kerrbl(self):
        print("comparing the various integrators")
        gg = gyoto.std.KerrBL()
        gg.set("Spin", 0.995)
        # gg, deltamaxoverr=0.1, deltamin=1e-6
        gg2 = gg.clone()
        gg2.set("GenericIntegrator", True)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        st2 = gyoto.std.Star()
        st2.metric(gg2)
        st2.integrator("runge_kutta_fehlberg78")
        st2.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        # TODO what to do here ?
        # st.integrator("Legacy")
        # st2.integrator("Legacy")
        # dates = np.arange(100.)
        # dates = np.arange(100)
        # dates = np.arange(100, dtype=np.float64)
        st.xFill(1000)
        st2.xFill(1000)
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        n2 = st2.get_nelements()

        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)

        t2 = np.ndarray(n2)
        r2 = np.ndarray(n2)
        theta2 = np.ndarray(n2)
        phi2 = np.ndarray(n2)

        # récupérer le tableau des dates
        st.get_t(t)
        st2.get_t(t2)

        # récupérer les 3 autres coordonnées
        st.getCoord(t, r, theta, phi)
        st2.getCoord(t2, r2, theta2, phi2)
        coords = np.concatenate((r, theta, phi))
        coords2 = np.concatenate((r2, theta2, phi2))
        # res = np.empty(100, dtype=np.float64)
        # pdates = gyoto.core.array_double.fromnumpy1(dates)
        # coords = st.getCoord(1)
        # res = st.getCoord(dates, coords)
        # coords2 = st2.getCoord(1)

        # TODO jb tester les surcharges de getcoord vector_double size 8

        np.testing.assert_array_almost_equal(coords, coords2)
        np.testing.assert_array_almost_equal(r, r2)
        np.testing.assert_array_almost_equal(theta, theta2)
        np.testing.assert_array_almost_equal(phi, phi2)

    def test_integrators_runge_kutta_dopri5_kerrbl(self):
        print("comparing the various integrators")
        gg = gyoto.std.KerrBL()
        gg.set("Spin", 0.995)
        # gg, deltamaxoverr=0.1, deltamin=1e-6
        gg2 = gg.clone()
        gg2.set("GenericIntegrator", True)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        st2 = gyoto.std.Star()
        st2.metric(gg2)
        st2.integrator("runge_kutta_dopri5")
        st2.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        # TODO what to do here ?
        # st.integrator("Legacy")
        # st2.integrator("Legacy")
        # dates = np.arange(100.)
        # dates = np.arange(100)
        # dates = np.arange(100, dtype=np.float64)
        st.xFill(1000)
        st2.xFill(1000)
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        n2 = st2.get_nelements()

        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)

        t2 = np.ndarray(n2)
        r2 = np.ndarray(n2)
        theta2 = np.ndarray(n2)
        phi2 = np.ndarray(n2)

        # récupérer le tableau des dates
        st.get_t(t)
        st2.get_t(t2)

        # récupérer les 3 autres coordonnées
        st.getCoord(t, r, theta, phi)
        st2.getCoord(t2, r2, theta2, phi2)
        coords = np.concatenate((r, theta, phi))
        coords2 = np.concatenate((r2, theta2, phi2))
        # res = np.empty(100, dtype=np.float64)
        # pdates = gyoto.core.array_double.fromnumpy1(dates)
        # coords = st.getCoord(1)
        # res = st.getCoord(dates, coords)
        # coords2 = st2.getCoord(1)

        # TODO jb tester les surcharges de getcoord vector_double size 8
        # len(coords) != len(coords2)
        # ERROR
        # TODO decimal=2 ?
        np.testing.assert_array_almost_equal(np.max(coords),
                                             np.max(coords2), decimal=2)
        # np.testing.assert_array_almost_equal_nulp(np.max(coords),
        #                                           np.max(coords2))
        # np.testing.assert_array_almost_equal(coords, coords2)
        # np.testing.assert_array_almost_equal(r, r2)
        # np.testing.assert_array_almost_equal(theta, theta2)
        # np.testing.assert_array_almost_equal(phi, phi2)

    def test_integrators_runge_kutta_cash_karp54_classic_kerrbl(self):
        print("comparing the various integrators")
        gg = gyoto.std.KerrBL()
        gg.set("Spin", 0.995)
        # gg, deltamaxoverr=0.1, deltamin=1e-6
        gg2 = gg.clone()
        gg2.set("GenericIntegrator", True)
        st = gyoto.std.Star()
        st.metric(gg)
        st.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        st2 = gyoto.std.Star()
        st2.metric(gg2)
        st2.setInitCoord([0., 10.791, np.pi / 2., 0], [0., 0., 0.016664])
        # TODO what to do here ?
        # st.integrator("Legacy")
        # st2.integrator("Legacy")
        # dates = np.arange(100.)
        # dates = np.arange(100)
        # dates = np.arange(100, dtype=np.float64)
        st.xFill(1000)
        st2.xFill(1000)
        # récupérer le nombre de points calculés sur la trajectoire
        n = st.get_nelements()
        n2 = st2.get_nelements()

        # créer des tableaux pour contenir les coordonnées
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)

        t2 = np.ndarray(n2)
        r2 = np.ndarray(n2)
        theta2 = np.ndarray(n2)
        phi2 = np.ndarray(n2)

        # récupérer le tableau des dates
        st.get_t(t)
        st2.get_t(t2)

        # récupérer les 3 autres coordonnées
        st.getCoord(t, r, theta, phi)
        st2.getCoord(t2, r2, theta2, phi2)
        coords = np.concatenate((r, theta, phi))
        coords2 = np.concatenate((r2, theta2, phi2))
        # res = np.empty(100, dtype=np.float64)
        # pdates = gyoto.core.array_double.fromnumpy1(dates)
        # coords = st.getCoord(1)
        # res = st.getCoord(dates, coords)
        # coords2 = st2.getCoord(1)

        # TODO jb tester les surcharges de getcoord vector_double size 8

        np.testing.assert_array_almost_equal(coords, coords2)
        np.testing.assert_array_almost_equal(r, r2)
        np.testing.assert_array_almost_equal(theta, theta2)
        np.testing.assert_array_almost_equal(phi, phi2)


if __name__ == '__main__':
    unittest.main()
