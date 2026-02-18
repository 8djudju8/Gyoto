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


# TODO add pdfPages ?

class TestStar(unittest.TestCase):
    def test_create_obj_Star(self):
        print("Star Astrobj in KerrBL metric")

        print("Attempting star construction:")
        st = gyoto.std.Star()
        print("Printing star:")
        print(st)

        print("Cloning...")
        st2 = st.clone()
        print("DONE.")

        print("Printing clone:")
        print(st2)

        print("Gyoto::Star pointer is at address: ")
        print(f"{st.getPointer()=}")

        print("Setting radius... ")
        st.radius(0.5)
        print("done.")

        print("Getting radius... ")
        if (st.radius() != 0.5):
            print("error CHECK FAILED")
        print("done.")

        print("Setting metric... ")
        metric = gyoto.std.KerrBL()
        metric.spin(0.)
        print("done.")
        st.metric(metric)
        print("Changing metric spin... ")
        metric.spin(0.7)
        if (metric.spin() != 0.7):
            print("error CHECK FAILED")
        metric.spin(0.995)
        if (metric.spin() != 0.995):
            print("error CHECK FAILED")
        print("done.")
        print("Setting initial condition... ")
        st.setInitCoord((0., 10.791, 1.5708, 0.), (0., 0., 0.0166637))
        print("done.")

        print("Setting integrator")
        if gyoto.HAVE_BOOST:
            st.integrator = "runge_kutta_fehlberg78"
            st.deltaMaxOverR(0.1)
        else:
            st.metric().deltamaxoverr(0.1)
        print("done")

        print("Computing orbit... ")
        st.xFill(800.)
        print("done.")

        n = st.get_nelements()

        print("Instanciating Screen... ")
        screen = gyoto.core.Screen()
        screen.metric(st.metric())
        print("done.")

        x = np.ndarray(n)
        y = np.ndarray(n)
        z = np.ndarray(n)

        print("Retrieving projected orbit... ")
        # data = st(get_skypos=screen)
        st.getSkyPos(screen, x, y, z)
        print("done.")

        print("Printing Star object:")
        print(st)

        # if (!nodisplay) {
        # print "Check it out (pausing for 1s)!"
        # plg,data(,2), data(,1)
        # limits
        # pause, 1000
        # winkill
        # }
        # plt.plot(data[:, 1], data[:, 0])
        # plt.plot(x, y)
        # plt.show()

        # TODO
        print("All in one call... ")
        # star2 = gyoto.std.Star()
        # star2.radius(0.5)
        # start2.metric = gyoto_KerrBL(spin=0.995),
        # metric = gyoto.std.KerrBL()
        # metric.spin(0.995)
        # star2.metric(metric)
        # star2.setInitCoord([0, 10.791, 1.5708, 0],
        #                   [0, 0, 0.0166637])
        # star2.xFill(800)
        # get_skypos=(
        # screen2=gyoto_Screen(metric=gyoto_KerrBL(spin=0.995)))
        print("NOPE done.")

        # if (!nodisplay) {
        # print "Check it out (pausing for 1s)!"
        # plg,data2(,2), data2(,1)
        # pause, 1000
        # winkill
        # }
        # data2 = star2
        # plt.plot(data2[:, 1], data2[:, 0])
        # // Free memroy to check with valgrind
        # //data=[]
        # //st=[]

        print("Star Astrobj in KerrBL metric")
