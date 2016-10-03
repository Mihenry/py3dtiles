# -*- coding: utf-8 -*-

import unittest

from py3dtiles import PCReader


class TestPCReader(unittest.TestCase):

    def test_read(self):
        # init reader
        reader = PCReader()
        reader.read_file('tests/pointCloudRGB.pnts')

        h = reader.header
        self.assertEqual(h.version, 1.0)
        self.assertEqual(h.tile_byte_length, 15176)
        self.assertEqual(h.ft_json_byte_length, 148)
        self.assertEqual(h.ft_bin_byte_length, 15000)
        self.assertEqual(h.bt_json_byte_length, 0)
        self.assertEqual(h.bt_bin_byte_length, 0)


def test_suite():
    return unittest.TestSuite([TestPCReader])

    if __name__ == '__main__':
        unittest.main()
