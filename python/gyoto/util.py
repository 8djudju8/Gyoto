'''Utility functions for Gyoto

Coord1dSet  -- easily initialize a gyoto.core.Coord1dset
rayTrace    -- a wrapper around gyoto.core.Scenery.rayTrace which
               hides most of its complexity
readScenery -- short hand for reading a Scenery XML file
'''


from gyoto import core
import numpy
import numbers

def Coord1dSet(k, res, sz):
    '''Easily initialize a gyoto.core.Coord1dset'''
    if (k is None):
        k=range(res//2-sz//2+1, res//2-sz//2+sz+1, 1)
    if type(k) is range:
        k=core.Range(k.start, k.stop-1, k.step)
    elif numpy.isscalar(k):
        if isinstance(k, numbers.Integral):
            k=core.Indices([k])
        elif isinstance(k, numbers.Real):
            k=core.Angles([k])
        else:
            raise ValueError('unknown scalar type')
    else:
        if all([isinstance(n, numbers.Integral) for n in k]):
            k=core.Indices(k)
        else:
            k=core.Angles(k)
    return k

def rayTrace(sc, i=None, j=None, coord2dset=core.Grid, width=None, height=None, fmt='\r j = '):
    '''Ray-trace scenery

First form:

results=scenery.rayTrace([coord2dset [,width, height] [,fmt]])

optional parameters:
coord2dset -- something to specify which part of the field to trace.
           can be: None to trace all pixels (default)
           a Coord2dSet instance
width, height -- horizontal and vertical resolution (overrides what
           is specified in scenery.screen().resolution()
fmt     -- prefix to be written in front of the row number for
           progress output

Output:
results -- dict containing the various requested quantities as per
           scenery.requestedQuantitiesString().

TODO:
Support and debug various kinds of coord2dset to allow ray-tracing
only part of the Scenery.


Second form:
'''
    if isinstance(j, core.AstrobjProperties):
        ij=i
        aop=j
        if not isinstance(coord2dset, type):
            ipct=coord2dset
        else:
            ipct=None
        core._core.Scenery_rayTrace(sc, i, j, ipct)
        return

    # If needed, read sc
    if type(sc) is str:
        sc=core.Factory(sc).scenery()

    # Determine resolution, width and height
    res=sc.screen().resolution()
    if width is not None:
        res = width
    else:
        width=res
    if height is not None and height > width:
        res = height
    else:
        height=res
    sc.screen().resolution(res)

    # Prepare coord2dset
    nx=None
    if isinstance(coord2dset, type):
        if not issubclass(coord2dset, core.Coord2dSet):
            raise TypeError("when coord2dset is a type, it must be a subclass of gyoto.core.Coord2dSet")
        if not isinstance(i, core.Coord1dSet):
            i=Coord1dSet(i, res, width)
        if not isinstance(j, core.Coord1dSet):
            j=Coord1dSet(j, res, height)
        try:
            coord2dset=coord2dset(i, j, fmt)
        except TypeError:
            coord2dset=coord2dset(i, j)
        nx=i.size()
        ntot=coord2dset.size()
        ny=ntot//nx
    elif isinstance(coord2dset, core.Coord2dSet):
        nx=ntot=coord2dset.size()
        ny=1
    else:
        raise TypeError('coord2dset must be a gyoto.core.Coord2dSet subclass or instance')

    # Prepare arrays to store results
    res = dict()
    aop=core.AstrobjProperties()
    aop.offset=nx*ny

    if sc.getSpectralQuantitiesCount():
        nsamples=sc.screen().spectrometer().nSamples()

    if 'Intensity' in sc.requestedQuantitiesString():
        intensity=numpy.zeros((ny, nx))
        pintensity=core.array_double_fromnumpy2(intensity)
        aop.intensity=pintensity
        res['Intensity']=intensity

    if 'EmissionTime' in sc.requestedQuantitiesString():
        time=numpy.zeros((ny, nx))
        ptime=core.array_double_fromnumpy2(time)
        aop.time=ptime
        res['EmissionTime'] = time

    if 'MinDistance' in sc.requestedQuantitiesString():
        distance=numpy.zeros((ny, nx))
        pdistance=core.array_double_fromnumpy2(distance)
        aop.distance=pdistance
        res['MinDistance'] = distance

    if 'FirstDistMin' in sc.requestedQuantitiesString():
        first_dmin=numpy.zeros((ny, nx))
        pfirst_dmin=core.array_double_fromnumpy2(first_dmin)
        aop.first_dmin=pfirst_dmin
        res['FirstDistMin'] = first_dmin

    if 'Redshift' in sc.requestedQuantitiesString():
        redshift=numpy.zeros((ny, nx))
        predshift=core.array_double_fromnumpy2(redshift)
        aop.redshift=predshift
        res['Redshift'] = redshift

    if 'ImpactCoords' in sc.requestedQuantitiesString():
        impactcoords=numpy.zeros((ny, nx, 16))
        pimpactcoords=core.array_double_fromnumpy3(impactcoords)
        aop.impactcoords=pimpactcoords
        res['ImpactCoords'] = impactcoords

    if 'User1' in sc.requestedQuantitiesString():
        user1=numpy.zeros((ny, nx))
        puser1=core.array_double_fromnumpy2(user1)
        aop.user1=puser1
        res['User1'] = user1

    if 'User1' in sc.requestedQuantitiesString():
        impactcoords=numpy.zeros((ny, nx))
        pimpactcoords=core.array_double_fromnumpy2(impactcoords)
        aop.impactcoords=pimpactcoords
        res['User1'] = impactcoords

    if 'User2' in sc.requestedQuantitiesString():
        user2=numpy.zeros((ny, nx))
        puser2=core.array_double_fromnumpy2(user2)
        aop.user2=puser2
        res['User2'] = user2

    if 'User3' in sc.requestedQuantitiesString():
        user3=numpy.zeros((ny, nx))
        puser3=core.array_double_fromnumpy2(user3)
        aop.user3=puser3
        res['User3'] = user3

    if 'User4' in sc.requestedQuantitiesString():
        user4=numpy.zeros((ny, nx))
        puser4=core.array_double_fromnumpy2(user4)
        aop.user4=puser4
        res['User4'] = user4

    if 'User5' in sc.requestedQuantitiesString():
        user5=numpy.zeros((ny, nx))
        puser5=core.array_double_fromnumpy2(user5)
        aop.user5=puser5
        res['User5'] = user5

    if 'Spectrum' in sc.requestedQuantitiesString():
        spectrum=numpy.zeros((nsamples, ny, nx))
        pspectrum=core.array_double_fromnumpy3(spectrum)
        aop.spectrum=pspectrum
        res['Spectrum'] = spectrum

    if 'SpectrumStokesQ' in sc.requestedQuantitiesString():
        stokesQ=numpy.zeros((nsamples, ny, nx))
        pstokesQ=core.array_double_fromnumpy3(stokesQ)
        aop.stokesQ=pstokesQ
        res['SpectrumStokesQ'] = stokesQ

    if 'SpectrumStokesU' in sc.requestedQuantitiesString():
        stokesU=numpy.zeros((nsamples, ny, nx))
        pstokesU=core.array_double_fromnumpy3(stokesU)
        aop.stokesU=pstokesU
        res['SpectrumStokesU'] = stokesU

    if 'SpectrumStokesV' in sc.requestedQuantitiesString():
        stokesV=numpy.zeros((nsamples, ny, nx))
        pstokesV=core.array_double_fromnumpy3(stokesV)
        aop.stokesV=pstokesV
        res['SpectrumStokesV'] = stokesV

    if 'BinSpectrum' in sc.requestedQuantitiesString():
        binspectrum=numpy.zeros((nsamples, ny, nx))
        pbinspectrum=core.array_double_fromnumpy3(binspectrum)
        aop.binspectrum=pbinspectrum
        res['BinSpectrum'] = binspectrum

    # Perform the actual ray-tracing
    sc.rayTrace(coord2dset, aop)

    return res

def readScenery(filename):
    '''Read Scenery from XML file'''
    return core.Factory(filename).scenery()

def writeObject(obj, filename):
    '''Write Gyoto object (e.g. Scenery) to XML file'''
    core.Factory(obj).write(filename)
