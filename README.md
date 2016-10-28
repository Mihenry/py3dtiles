# py3dtiles

Python module to manage 3DTiles format.

For now, only the Point Cloud specification is supported.


## Install

### From sources

To use py3dtiles from sources:

````
$ sudo apt-get install libgdal-dev
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

Moreover, a utility class *TileReader* is available to read a *.pnts* file as
well as simple command line tool to retrieve basic information about a Point Cloud
file **py3dtiles_info.py**.


**How to read a .pnts file**

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
>>> # extract positions and colors of the first point
>>> f = ft.feature(0)
>>> f
<py3dtiles.feature_table.Feature>
>>> f.positions
{'Y': 4.4896851, 'X': 2.19396, 'Z': -0.17107764}
>>> f.colors
{'Green': 243, 'Red': 44, 'Blue': 209}
````

**How to write a .pnts file**

To write a Point Cloud file, you have to build a numpy array with the
corresponding data type.

````python
>>> from py3dtiles import Feature
>>> import numpy as np
>>>
>>> # create the numpy dtype for positions with 32-bit floating point numbers
>>> dt = np.dtype([('X', '<f4'), ('Y', '<f4'), ('Z', '<f4')])
>>>
>>> # create a position array
>>> position = np.array([(4.489, 2.19, -0.17)], dtype=dt)
>>>
>>> # create a new feature from a uint8 numpy array
>>> f = Feature.from_array(dt, position.view('uint8'))
>>> f
<py3dtiles.feature_table.Feature>
>>> f.positions
{'Y': 2.19, 'X': 4.489, 'Z': -0.17}
>>>
>>> # create a tile directly from our feature. None is for "no colors".
>>> t  = Tile.from_features(dt, None, [f])
>>>
>>> # the tile is complete
>>> t.body.feature_table.header.to_json()
{'POINTS_LENGTH': 1, 'POSITION': {'byteOffset': 0}}
>>>
>>> # to save our tile as a .pnts file
>>> t.save_as("mypoints.pnts")
````

**How to use py3dtiles_info.py**

If we want to retrieve basic information about the file *mypoints.pnts*
previously created:

````
$ ./tools/py3dtiles_info.py mypoints.pnts
Tile Header
-----------
Magic Value:  pnts
Version:  1
Tile byte length:  88
Feature table json byte length:  48
Feature table bin byte length:  12

Feature Table Header
--------------------
{'POINTS_LENGTH': 1, 'POSITION': {'byteOffset': 0}}

First point
-----------
{'Y': 2.1900001, 'X': 4.4889998, 'Z': -0.17}
````
