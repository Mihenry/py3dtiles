# py3dtiles

Python module to manage 3DTiles format.

For now, only the Point Cloud specification is supported.


## Install

### From sources

To use py3dtiles from sources:

````bash
$ git clone https://github.com/pblottiere/py3dtiles
$ cd py3dtiles
$ virtualenv -p /usr/bin/python3 venv
$ . venv/bin/activate
(venv)$ pip install -e
````

If you wan to run unit tests:

````
(venv)$ pip install nose
(venv)$ nosetests
...

````

## Specifications

### Point Cloud

Point Cloud Tile Format: https://github.com/AnalyticalGraphicsInc/3d-tiles/tree/master/TileFormats/PointCloud

<p align="center">
<img align="center" src="https://github.com/pblottiere/py3dtiles/blob/master/docs/pc_layout.png" width="700">
</p>

The py3dtiles module provides some classes to fit into the specification:
- *Tile* with a header *TileHeader* and a body *TileBody*
- *TileHeader* represents the first 28 bytes (magic value, version, ...)
- *TileBody* contains the feature table *FeatureTable* and the batch table (not supported for now)
- *FeatureTable* with a header *FeatureTableHeader* and a *FeatureTableBody*
- *FeatureTableBody* which contains features of type *Feature*

Moreover, a utility class *TileReader* is available to read a *.pnts* file.

````python
>>> from py3dtiles import TileReader
>>>
>>> filename = 'tests/pointCloudRGB.pnts'
>>>
>>> # read the file
>>> tile = TileReader().read_file(filename)
>>>
>>> # tile is an instance of the Tile class
>>> tile
<py3dtiles.tile.Tile>
>>>
>>> # extract information about the tile header
>>> th = tile.header
>>> th
<py3dtiles.tile.TileHeader>
>>> th.magic_value
'pnts'
>>> th.tile_byte_length
15176
>>>
>>> # extract the feature table
>>> ft = tile.body.feature_table
>>> ft
<py3dtiles.feature_table.FeatureTable
>>>
>>> # display feature table header
>>> ft.header.to_json()
{'RTC_CENTER': [1215012.8828876738, -4736313.051199594, 4081605.22126042],
'RGB': {'byteOffset': 12000}, 'POINTS_LENGTH': 1000, 'POSITION': {'byteOffset': 0}}
>>>
````

To write a Point Cloud file, you have to build a numpy array with the corresponding dtype:

````
> python3
# from py3dtiles import TileReader
TODO
````


#### Tools

