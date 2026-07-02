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
#    along with Gyoto.  If not, see <http:# www.gnu.org/licenses/>.
#
import os
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

GYOTO_EXAMPLES_DIR = os.path.join("./", "../doc/examples/")
PD_XML = GYOTO_EXAMPLES_DIR + "example-polish-doughnut.xml"
print(PD_XML)


class TestPolishDoughnut(unittest.TestCase):
    def test_create_obj_PolishDoughnut(self):
        print("Polish doughnut AstroObj")
        print("Creating default PolishDoughnut... ")
        pd = gyoto.std.PolishDoughnut()
        print("done")
        print("Printing object:")
        assert pd
        print(pd)
        #  print( "Setting lambda to 2... ")
        #  pd.lambda(2)
        #  print( "print("done")."

        #  write, format = "%s", "Checking value of lambda... "
        #  if (pd(get_lambda=1)==2) print( "print("done")."; \
        #   else error, "CHECK FAILED!"

        print("Instanciating Kerr metric... ")
        gg = gyoto.std.KerrBL()
        print("done")

        print("Attaching metric to doughnut... ")
        pd.metric(gg)
        print("done")

        print("Checking attached metric... ")
        self.assertIsNotNone(pd.metric())
        # if (pd.metric() == KerrBL):
        self.assertEqual(pd.metric().getPointer(), gg.getPointer())

        print("Printing object:")
        print(pd)

    def test_create_PolishDoughnut_from_file(self):
        # if gyoto.GYOTO_USE_XERCES and gyoto.GYOTO_USE_UDUNITS:
        print("Creating PolishDoughnut from file...")
        print("Reading PolishDoughnut scenery... ")
        sc = gyoto.core.Factory(PD_XML).scenery()
        print("done")
        pd = gyoto.core.Factory(PD_XML).astrobj()
        print("done")

        assert pd
        print("Printing object:")
        print(pd)

        print("Creating spectro...")
        spect = gyoto.spectrometer.Uniform()
        spect.kind("freqlog")
        spect.nSamples(2)
        spect.band([10, 14], "Hz")
        # spect.unit("Hz") => no attribute
        print("Setting spectro...")
        # sc.screen.spectro(
        #    gyoto_SpectroUniform(kind="freqlog",
        #                         nsamples=2,
        #                         band=[10, 14],
        #                         unit="Hz")
        #                )
        sc.screen().spectrometer(spect)
        sc.astrobj().opticallyThin(True)
        print("done")

        print("Ray-tracing scenery... ")
        # TODO
        # img = np.average(sc[:, :]["Spectrum"], 2)
        img = sc[:, :]["Spectrum"]
        print("done")

        print("Displaying image... ")
        plt.imshow(img[0, :, :])
        plt.show()
        # fma; pli, img
        print("done")

        # pause, 1000

        print("Change spectro samples...")
        # spect = gyoto.spectrometer.Uniform()
        # spect.kind("freqlog")
        # spect.nSamples(2)
        # spect.band([10, 14], "Hz")
        spect.nSamples(10)
        # sc.screen.spectro(
        #    gyoto_SpectroUniform(kind="freqlog",
        #                         nsamples=10,
        #                         band=[10, 14],
        #                         unit="Hz")
        #                )
        sc.requestedQuantitiesString("Spectrum[J.m-2.s-1.sr-1.Hz-1]")
        print("Integrating one spectrum with radiative transfer...\n")
        # s1 = sc[10, 15]["Spectrum[J.m-2.s-1.sr-1.Hz-1]"]
        s1 = sc[10, 14]["Spectrum"]
        print("done")
        midpoints = np.zeros(0)
        sc.screen().spectrometer().getMidpoints(midpoints, "Hz")
        widths = np.zeros(0)
        sc.screen().spectrometer().getWidths(widths, "Hz")
        # TODO
        # fma
        # logxy, 1, 1
        # plg, (s1*widths), midpoints, color="red"
        # xytitles, "Frequency [Hz]"
        y = s1 * widths
        x = midpoints
        plt.plot(x, y)
        plt.show()
        print("Integrating one bin spectrum with radiative transfer...\n")
        sc.requestedQuantitiesString("BinSpectrum[J.m-2.s-1.sr-1]")
        s2 = sc[10, 15]["BinSpectrum"]
        print("done")

    @unittest.skip("no spectro")
    # TODO a ne pas faire fonctionner
    def test_create_obj_spectro_PolishDoughnut(self):

        sc = gyoto.core.Factory(PD_XML).scenery()
        spect = gyoto.spectrometer.Uniform()
        spect.kind("freqlog")
        spect.nSamples(2)
        spect.band([10, 14], "Hz")
        sc.screen().spectrometer(spect)
        sc.astrobj().opticallyThin(True)

        channels = sc.screen().spectrometer().getChannelBoundaries()
        widths = sc.screen().spectrometer().getWidths()
        bands = sc.screen().spectrometer().getBand()
        # s22 = np.zeros(len(s2) * 2)
        # s22[::2] = s2
        # s22[2::2] = s2
        # chan2 = np.zeros(len(s2) * 2)
        # chan2[::1] = channels[0, :]
        # chan2[1::2] = channels[1, :]
        # plg, s22, chan2
        # if (batch()):
        #    pause, 1000
        #    winkill,0
        print("PolishDoughnut Astrobj")


if __name__ == '__main__':
    unittest.main()
