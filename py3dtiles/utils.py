# -*- coding: utf-8 -*-

import numpy as np
from .tile import Tile
from osgeo import osr, ogr


def convert_to_ecef(x, y, z, epsg_input):
    # init spatial converter
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(epsg_input)

    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(4978)  # ECEF

    coordTrans = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

    wkt = "POINT ({0} {1} {2})".format(x, y, z)
    point = ogr.CreateGeometryFromWkt(wkt)
    point.Transform(coordTrans)

    return [point.GetX(), point.GetY(), point.GetZ()]


class TileReader(object):

    def read_file(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            arr = np.frombuffer(data, dtype=np.uint8)
            return self.read_array(arr)
        return None

    def read_array(self, array):
        return Tile.from_array(array)
