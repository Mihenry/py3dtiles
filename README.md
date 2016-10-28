# py3dtiles

Python module to manage 3DTiles format.

For now, only the Point Cloud specification is supported.


## Clone, Install and Tests

````
> git clone https://github.com/pblottiere/py3dtiles
> cd py3dtiles
> virtualenv -p python3 venv
> source venv/bin/activate
> pip install -e
> python3 setup.py test
> python3 setup.py install
````


## Specifications

### Point Cloud

Spec: https://github.com/AnalyticalGraphicsInc/3d-tiles/tree/master/TileFormats/PointCloud

Point CLoud files: 

#### TileReader class

If you want to read a Point Cloud file (*.pnts* extension) in python, you can use the **TileReader** class:

````
> python3
# from py3dtiles import TileReader
#
# open the file
# filename = 'pointCloudRGB.pnts'
# tile = TileReader().read_file(filename)
#
# explore the tile header
# th = tile.header
# print(th.magic_value)
TODO
# retrieve the feature tableùd'ssssssssssssss
# ft = tile.body.feature_table
# ft.header.to_json()
TODO
# feature = ft.feature(0)
# print(feature.positions)
# TODO
````

To write a Point Cloud file, you have to build a numpy array with the corresponding dtype:

````
> python3
# from py3dtiles import TileReader
TODO
````


#### Tools

