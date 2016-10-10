# -*- coding: utf-8 -*-

import argparse
import liblas
import pyproj
import numpy as np
import sys

from py3dtiles import convert_to_ecef, Feature, Tile


def las2pnts(filename, epsg_input):

    # open las file
    f = liblas.file.File(filename, mode='r')

    # extract informations
    npoints = f.header.point_records_count

    # extract min/max in ecef coordinates
    bb_min = f.header.min
    bb_max = f.header.max

    bb_min = convert_to_ecef(bb_min[0], bb_min[1], bb_min[2], epsg_input)
    bb_max = convert_to_ecef(bb_max[0], bb_max[1], bb_max[2], epsg_input)

    xcenter = (bb_max[0] - bb_min[0])/2 + bb_min[0]
    ycenter = (bb_max[1] - bb_min[1])/2 + bb_min[1]
    zcenter = (bb_max[2] - bb_min[2])/2 + bb_min[2]
    rtc = [xcenter, ycenter, zcenter]

    # extract features
    i = 0
    features = []
    pdt = np.dtype([('X', '<f4'), ('Y', '<f4'), ('Z', '<f4')])
    cdt = np.dtype([('Red', 'u1'), ('Green', 'u1'), ('Blue', 'u1')])
    for pt in f:
        print("{0}/{1}\r".format(i, npoints), end='')
        [x, y, z] = convert_to_ecef(pt.x, pt.y, pt.z, epsg_input)
        pos_arr = np.array([(x-xcenter, y-ycenter, z-zcenter)], dtype=pdt).view('uint8')
        col_arr = np.array([(0, 0, 0)], dtype=cdt).view('uint8')
        features.append(Feature.from_array(pdt, pos_arr, cdt, col_arr))
        i += 1

    tile = Tile.from_features(pdt, cdt, features)
    tile.body.feature_table.header.rtc = [xcenter, ycenter, zcenter]

    output = "/tmp/las2pnts.pnts"
    tile.save_as(output)
    print("Output file saved as ", output)


if __name__ == '__main__':

    # arg parse
    descr = 'Convert a LAS file to a pnts file and a tileset'
    parser = argparse.ArgumentParser(description=descr)

    f_help = 'LAS filename'
    parser.add_argument('f', metavar='f', type=str, help=f_help)

    epsg_help = 'epsg input (\'2950\' for example)'
    parser.add_argument('e', metavar='e', type=int, help=epsg_help)

    args = parser.parse_args()

    las2pnts(args.f, args.e)
