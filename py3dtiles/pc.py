# -*- coding: utf-8 -*-

import numpy as np
from .header import TileHeader
from .feature import FeatureTable


class PC(object):

    def __init__(self):
        self.raw = []
        self.header = None
        self.body = None


class PCReader(PC):

    def __init__(self):
        PC.__init__(self)

    def read_file(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            arr = np.frombuffer(data, dtype=np.uint8)
            self.read_array(arr)

    def read_array(self, array):
        self.raw = array

        # extract header
        self.header = TileHeader(array[0:TileHeader.BYTELENGTH])

        # check validity
        if self.header.magic_value != "pnts":
            raise RuntimeError("Array is not described in 3D tiles format")

        if self.header.tile_byte_length != len(array):
            raise RuntimeError("Invalid byte length in header")

        # extract body
        ft_length = self.header.ft_json_byte_length \
            + self.header.ft_bin_byte_length
        ft_arr = array[TileHeader.BYTELENGTH:TileHeader.BYTELENGTH+ft_length]
        self.body = FeatureTable(self.header.ft_json_byte_length, ft_arr)
