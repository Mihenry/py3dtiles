# -*- coding: utf-8 -*-

import numpy as np
from .tile import Tile


class TileReader(object):

    def read_file(self, filename):
        with open(filename, 'rb') as f:
            data = f.read()
            arr = np.frombuffer(data, dtype=np.uint8)
            return self.read_array(arr)
        return None

    def read_array(self, array):
        return Tile.from_array(array)
