# -*- coding: utf-8 -*-

import struct


class TileHeader(object):

    BYTELENGTH = 28

    def __init__(self, array):
        if len(array) != 28:
            raise RuntimeError("Invalid header length")

        self.magic_value = bytes(array[0:4]).decode("utf-8")
        self.version = struct.unpack("i", array[4:8])[0]
        self.tile_byte_length = struct.unpack("i", array[8:12])[0]
        self.ft_json_byte_length = struct.unpack("i", array[12:16])[0]
        self.ft_bin_byte_length = struct.unpack("i", array[16:20])[0]
        self.bt_json_byte_length = struct.unpack("i", array[20:24])[0]
        self.bt_bin_byte_length = struct.unpack("i", array[24:28])[0]

    def info(self):
        print("HEADER")
        print("------")
        print("Version: ", self.version)
        print("Tile byte length: ", self.tile_byte_length)
        print("Feature table json byte length: ", self.ft_json_byte_length)
        print("Feature table binary byte length: ", self.ft_bin_byte_length)
        print("Batch table json byte length: ", self.bt_json_byte_length)
        print("Batch table binary byte length: ", self.bt_bin_byte_length)
