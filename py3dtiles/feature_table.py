# -*- coding: utf-8 -*-

import json
from enum import Enum
import numpy as np


class Feature(object):

    def __init__(self, semantic, positions, colors):
        """
        Parameters
        ----------
        semantic : Semantics

        positions : numpy.array

        colors : numpy.array
        """

        # extract positions
        self.positions = {}
        dtype = semantic.positions_dtype
        off = 0
        for d in dtype.names:
            itemsize = dtype[d].itemsize
            data = np.array(positions[off:off+itemsize]).view(dtype[d])[0]
            off += itemsize
            self.positions[d] = data

        # extract colors
        self.colors = {}
        if semantic.colors != SemanticPoint.NONE:
            dtype = semantic.colors_dtype
            off = 0
            for d in dtype.names:
                itemsize = dtype[d].itemsize
                data = np.array(colors[off:off+itemsize]).view(dtype[d])[0]
                off += itemsize
                self.colors[d] = data


class SemanticPoint(Enum):

    NONE = 0
    POSITION = 1
    POSITION_QUANTIZED = 2
    RGBA = 3
    RGB = 4
    RGB565 = 5
    NORMAL = 6
    NORMAL_OCT16P = 7
    BATCH_ID = 8


class FeatureTableHeader(object):

    def __init__(self):
        # point semantics
        self.positions = SemanticPoint.POSITION
        self.positions_offset = 0
        self.positions_dtype = None

        self.colors = SemanticPoint.NONE
        self.colors_offset = 0
        self.colors_dtype = None

        self.normal = SemanticPoint.NONE
        self.normal_offset = 0
        self.normal_dtype = None

        # global semantics
        self.points_length = None
        self.rtc = None

    @staticmethod
    def from_array(array):
        """
        Parameters
        ----------
        array : numpy.array
            Json in 3D Tiles format. See py3dtiles/doc/semantics.json for an
            example.

        Returns
        -------
        fth : FeatureTableHeader
        """

        jsond = json.loads(array.tostring().decode('utf-8'))

        fth = FeatureTableHeader()

        # search position
        if "POSITION" in jsond:
            fth.positions = SemanticPoint.POSITION
            fth.positions_offset = jsond['POSITION']['byteOffset']
            fth.positions_dtype = np.dtype([('X', np.float32),
                                            ('Y', np.float32),
                                            ('Z', np.float32)])
        elif "POSITION_QUANTIZED" in jsond:
            fth.positions = SemanticPoint.POSITION_QUANTIZED
            fth.positions_offset = jsond['POSITION_QUANTIZED']['byteOffset']
            fth.positions_dtype = np.dtype([('X', np.uint16),
                                            ('Y', np.uint16),
                                            ('Z', np.uint16)])
        else:
            fth.positions = SemanticPoint.NONE
            fth.positions_offset = 0
            fth.positions_dtype = None

        # search colors
        if "RGB" in jsond:
            fth.colors = SemanticPoint.RGB
            fth.colors_offset = jsond['RGB']['byteOffset']
            fth.colors_dtype = np.dtype([('Red', np.uint8),
                                         ('Green', np.uint8),
                                         ('Blue', np.uint8)])
        else:
            fth.colors = SemanticPoint.NONE
            fth.colors_offset = 0
            fth.colors_dtype = None

        # points length
        if "POINTS_LENGTH" in jsond:
            fth.points_length = jsond["POINTS_LENGTH"]

        # RTC (Relative To Center)
        if "RTC" in jsond:
            fth.rtc = jsond['RTC']
        else:
            fth.rtc = None

        return fth


class FeatureTableBody(object):

    def __init__(self):
        self.positions_arr = []
        self.positions_itemsize = 0

        self.colors_arr = []
        self.colors_itemsize = 0

    @staticmethod
    def from_array(fth, array):
        """
        Parameters
        ----------
        header : FeatureTableHeader

        array : numpy.array

        Returns
        -------
        ftb : FeatureTableBody
        """

        b = FeatureTableBody()

        npoints = fth.points_length

        # extract positions
        pos_size = fth.positions_dtype.itemsize
        pos_offset = fth.positions_offset
        b.positions_arr = array[pos_offset:pos_offset+npoints*pos_size]
        b.positions_itemsize = pos_size

        # extract colors
        if fth.colors != SemanticPoint.NONE:
            col_size = fth.colors_dtype.itemsize
            col_offset = fth.colors_offset
            b.colors_arr = array[col_offset:col_offset+col_size*npoints]
            b.colors_itemsize = col_size

        return b

    def positions(self, n):
        itemsize = self.positions_itemsize
        return self.positions_arr[n*itemsize:(n+1)*itemsize]

    def colors(self, n):
        if len(self.colors_arr):
            itemsize = self.colors_itemsize
            return self.colors_arr[n*itemsize:(n+1)*itemsize]
        return []


class FeatureTable(object):

    def __init__(self):
        self.header = FeatureTableHeader()
        self.body = FeatureTableBody()

    def npoints(self):
        return self.header.points_length

    @staticmethod
    def from_array(th, array):
        """
        Parameters
        ----------
        th : TileHeader

        array : numpy.array

        Returns
        -------
        ft : FeatureTable
        """

        # build feature table header
        fth_len = th.ft_json_byte_length
        fth_arr = array[0:fth_len]
        fth = FeatureTableHeader.from_array(fth_arr)

        # build feature table body
        ftb_len = th.ft_bin_byte_length
        ftb_arr = array[fth_len:fth_len+ftb_len]
        ftb = FeatureTableBody.from_array(fth, ftb_arr)

        # build feature table
        ft = FeatureTable()
        ft.header = fth
        ft.body = ftb

        return ft

    def feature(self, n):
        pos = self.body.positions(n)
        col = self.body.colors(n)
        return Feature(self.header, pos, col)
