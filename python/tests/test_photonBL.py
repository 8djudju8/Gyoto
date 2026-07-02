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
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

gyoto.core.requirePlugin('stdplug')


class TestPhotonBL(unittest.TestCase):
    def test_create_obj_PhotonBL(self):
        print("Photon in KerrBL metric")
        aa = 0.
        gg = gyoto.std.KerrBL()
        gg.spin(aa)
        gg2 = gg.clone()
        sc = gyoto.core.Scenery()
        sc.metric(gg)
        print(f"{sc.NormTol=}")
        print("Creating Photon: ")
        ph = gyoto.core.Photon()
        self.assertEqual(ph.getMass(), 0.0)
        # if (ph()):
        #    print("done")
        # else:
        #    print("error PREVIOUS CHECK FAILED")

        # gg.deltaMin(1E-10)
        # gg.set("deltaMin", 1E-10)
        gg.deltaMin()
        sc.tMin(-1e-6)
        sc.absTol(1e-16)
        sc.relTol(1e-16)
        print("Attaching metric: ")
        ph.metric(gg)
        assert ph.getProperties() is not None
        assert ph

        # initial conditions :
        ri = 6
        thetai = np.pi / 2.
        phii = 0.

        # ttravel = r0
        ti = 0.
        pri = 0.  # canonical momentum
        pthetai = 0.
        # yinit = [ti, ri, thetai, phii, ti, pri, pthetai]
        cst = [1, 0.921103, 2., 0.]  # 4 Kerr cst of motion a, E, L, Q

        if cst[3] == 0.:
            cst = np.append(cst, 1.)
        else:
            cst = np.append(cst, 1. / cst[3])

        yinit = [ti, ri, thetai, phii, -cst[1], pri, pthetai, cst[2]]
        yout = np.zeros(8)
        coord = np.zeros(8)

        print(f"{ph.get_nelements()=}")
        print(f"{yout=} {coord=}")
        print(f"{yout.shape=} {coord.shape=}")
        print(f"{cst=}")
        print("Checking gyoto_Kerr_MakeCoord: ")
        # coord = gg(makecoord=yinit, cst)
        gg.MakeCoord(yinit, cst, coord)
        print(f"{yout=} {coord=}")
        print(f"{yout.shape=} {coord.shape=}")

        # if (abs((coord-[0,10.791,1.5708,0,1.12641,0,0,0.0187701]))(max)<1e-6)
        if np.max(abs((coord
                       - [0, 6, 1.5708, 0, 1.38165, 0, 0, 0.0555556]))) < 1e-5:
            print("done.\n")
        else:
            print("error PREVIOUS CHECK FAILED 1")

        print("Setting metric spin")
        gg.spin(0.95)
        print("done")
        print("Computing initial coordinate")
        gg.MakeCoord(yinit, cst, coord)
        print("done")
        print(f"{yout=} {coord=}")
        pos = coord[:5]
        v = coord[5:] / coord[4]
        print(f"{pos=}")
        print(f"{v=}")
        print("Checking gyoto_Star")
        st = gyoto.std.Star()
        st.metric(gg)
        st.radius(1.)
        st.initCoord(np.append(pos, v))
        print("done")

        print("Trying gyoto_Star_xFill")
        st.xFill(10.)
        print("done")

        # TODO add scenery + rayTrace
        # plot hitmap
        # add get_xyz and plot(x, y)

        # Computing position of star at a given proper time :
        # time=212.4034;//proper time
        # print( "Checking gyoto_Star_position: "
        # pos=gyoto_Part_position(st,time)
        # pos
        # if (abs(pos-
        # [10.5718661339679, 1.57079398752261, 59.5795847453848])(max)<1e-5)
        #  print("print("done").\n"; else error, "PREVIOUS CHECK FAILED"

        # Ray tracing

        print("Checking gyoto_Metric_setObserverPos: ")
        # screen = gyoto.core.Screen()
        screen = sc.screen()
        screen.metric(gg)
        screen.setObserverPos([1000., 100., 0.05, 0.])
        print("done.\n")
        print("Checking gyoto_Metric_setSpin: ")
        gg.spin(0.)
        gg.deltaMin(40)
        print("done.\n")
        print("Checking gyoto_Star(): ")
        orbit = gyoto.std.Star()
        orbit.metric(gg)
        orbit.radius(2)
        orbit.setInitCoord((600., 6., 1.57, 0.), (0., 0., 0.068041381745))
        print("done.\n")
        sc.astrobj(orbit)
        N = 21
        delta = np.pi / (10. * N)
        screen.set("FieldOfView", np.pi / 10.)
        screen.resolution(21)
        gg.set("GenericIntegrator", True)
        i = 15
        j = 9
        xscr = delta * (i - (N + 1) / 2.)
        yscr = delta * (j - (N + 1) / 2.)
        print("Checking gyoto_Photon_setInitialCondition: ")
        ph2 = gyoto.core.Photon()
        ph2.metric(gg)
        ph2.astrobj(orbit)
        ph2.setInitialCondition(gg, ph2.astrobj(), screen, i, j)
        # ph2.setInitialCondition(sc.metric(), sc.astrobj(), sc.screen, i, j)
        ph1 = gyoto.core.Photon()
        ph1.metric(gg)
        ph1.astrobj(orbit)
        print(f"{ph1.astrobj()=}")
        print(f"{ph2.metric()=}")
        print(f"{gg=}")
        # ph1.initCoord(screen, -xscr, yscr)
        ph1.setInitialCondition(ph1.metric(), ph1.astrobj(),
                                screen, -xscr, yscr)
        # ph1.setInitialCondition(sc.metric(), sc.astrobj(),
        # sc.screen, -xscr, yscr)
        # ph2.initCoord(screen, i, j)
        print("done.\n")
        print("Checking gyoto_Photon(delta=1): ")
        print("done.\n")
        print("Checking gyoto_Photon(is_hit=1): ")
        hit1 = ph1.hit()
        hit2 = ph2.hit()
        n1 = ph1.get_nelements()
        n2 = ph2.get_nelements()
        print(f"{n1=}")
        print(f"{n2=}")
        print(f"hit1: {hit1}")
        print(f"hit2: {hit2}")
        if (ph1.hit() and ph2.hit()):
            print("done.\n")
        else:
            print("error PREVIOUS CHECK FAILED 2")
        print("_________________________")
        # n1 = ph1.get_nelements()
        # n2 = ph2.get_nelements()
        wl = gyoto.std.Star(sc.astrobj())
        wl.xFill(1000)
        n = wl.get_nelements()
        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)
        wl.get_xyz(x, y, z)
        plt.plot(x, y)
        plt.show()
        # hitmap2 =
        # hitmap1 =
        hitmap = np.zeros((N, N))
#        hitmap1 = np.array((0, N, N))
#        hitmap2 = np.array((0, N, N))
        ph = gyoto.core.Photon()
        ph.metric(gg)
        ph.astrobj(orbit)
        for i in range(1, N):
            print(f"*** Column {i} ***\n")
            xscr = delta * (i - (N + 1) / 2.)
            for j in range(1, N):
                yscr = delta * (j - (N + 1) / 2.)
                ph.setInitialCondition(ph.metric(), ph.astrobj(),
                                       screen, -xscr, yscr)
                # ph.initCoord(screen, -xscr, yscr)
                ph.tMin(0.)
                ph1.setInitialCondition(ph1.metric(), ph1.astrobj(),
                                        screen, -xscr, yscr)
                ph2.setInitialCondition(ph2.metric(), ph2.astrobj(),
                                        screen, i, j)
                # ph1.initCoord(screen, -xscr, yscr)
                # ph2.initCoord(screen, i, j)
                ph.delta(1.)
                hitmap[i, j] = ph.hit()
        ph2 = None

        # Check that changing spin can be print("done") on attached metric
        ph1.metric() == ph1.metric()
        ph1.xFill(0.)
        n = ph1.get_nelements()
        # txyz = ph1.get_txyz()
        t = np.ndarray(n)
        r = np.ndarray(n)
        theta = np.ndarray(n)
        phi = np.ndarray(n)
        ph1.get_t(t)
        ph.getCoord(t, r, theta, phi)
        plt.plot(t, r)
        plt.show()
        # plt.plot(txyz[2, :], txyz[1, :])
        ph2 = ph1.clone()
        gg2 = gg.clone()
        print("Mutating metric spin... ")
        gg.spin(0.5)
        print("done.")
        gg2.spin(0.5)
        ph2.metric(gg2)

        ph1 = None
        ph2 = None

        # CLONES AND HOOKS

        print("_________________________")

        print("End Photon in KerrBL metric")


if __name__ == '__main__':
    unittest.main()
