# -*- coding: utf-8 -*-

import unittest

from py3dtiles import TileReader


class TestTileReader(unittest.TestCase):

    def test_read(self):
        # init reader
        tile = TileReader().read_file('tests/pointCloudRGB.pnts')

        self.assertEqual(tile.header.version, 1.0)
        self.assertEqual(tile.header.tile_byte_length, 15176)
        self.assertEqual(tile.header.ft_json_byte_length, 148)
        self.assertEqual(tile.header.ft_bin_byte_length, 15000)
        self.assertEqual(tile.header.bt_json_byte_length, 0)
        self.assertEqual(tile.header.bt_bin_byte_length, 0)

        feature_table = tile.body.feature_table
        feature = feature_table.feature(0)
        dcol_res = {'Red': 44, 'Blue': 209, 'Green': 243}
        self.assertDictEqual(dcol_res, feature.colors)


def test_suite():
    return unittest.TestSuite([TestTileReader])

    if __name__ == '__main__':
        unittest.main()
