# -*- coding: utf-8 -*-

import json
import numpy as np


class Dimension(object):

    def __init__(self, type, name, size):
        self.type = type
        self.name = name
        self.size = size

    def json(self):
        d = {}
        d['type'] = self.type
        d['name'] = self.name
        d['size'] = self.size
        return json.dumps(d)

    def value(self):
        pass


class Schema(object):

    def __init__(self):
        self.dims = []

    def add(self, d):
        self.dims.append(d)

    def json(self):
        return json.dumps(self.dims)

    def dimsize(self, dimname):
        for d in self.dims:
            if d.name == dimname:
                return d.size
        return None

    def dim(self, dimname):
        for d in self.dims:
            if d.name == dimname:
                return d
        return None

    def numpy_description(self):
        formats = []
        names = []

        for d in self.dims:
            t = d.type
            if t == 'floating':
                t = 'f'
            elif t == 'unsigned':
                t = 'u'
            else:
                t = 'i'
            f = '%s%d' % (t, d.size)
            names.append(d.name)
            formats.append(f)

        return np.dtype({'names': names, 'formats': formats})


class Point(object):

    def __init__(self, schema, arr):
        self.dtype = schema.numpy_description()

        self.data = {}
        offset = 0
        for d in self.dtype.names:
            itemsize = self.dtype[d].itemsize
            a = np.array(arr[offset:offset+itemsize]).view(self.dtype[d])[0]
            offset += itemsize
            self.data[d] = a


class FeatureTableHeader(object):

    def __init__(self, arr):
        self.json = json.loads(arr.tostring().decode('utf-8'))

        self.schema = Schema()
        self._init_schema()
        self.npoints = self.json['POINTS_LENGTH']

    def _init_schema(self):
        if 'POSITION' in self.json:
            dx = Dimension('floating', 'X', 4)
            self.schema.add(dx)

            dy = Dimension('floating', 'Y', 4)
            self.schema.add(dy)

            dz = Dimension('floating', 'Z', 4)
            self.schema.add(dz)

        if 'RGB' in self.json:
            dr = Dimension('unsigned', 'Red', 1)
            self.schema.add(dr)

            dg = Dimension('unsigned', 'Green', 1)
            self.schema.add(dg)

            db = Dimension('unsigned', 'Blue', 1)
            self.schema.add(db)


class FeatureTableBody(object):

    def __init__(self, header, arr):
        npoints = header.npoints
        schema = header.schema

        # extract positions (mandatory in header)
        self.pos_size = schema.dimsize('X')*3
        self.positions = arr[0:npoints*self.pos_size]

        # RGB: uint8[3] : optional
        self.colors = []
        self.col_size = 0
        if schema.dim('Red'):
            self.col_size = schema.dimsize('Red')*3
            off = header.json['RGB']['byteOffset']
            self.colors = arr[off: off + npoints*self.col_size]

    def point(self, n):
        pt_arr = []

        pos_arr = self.positions[n*self.pos_size:(n+1)*self.pos_size]
        pt_arr.extend(pos_arr)

        if len(self.colors):
            col_arr = self.colors[n*self.col_size:(n+1)*self.col_size]
            pt_arr.extend(col_arr)

        return pt_arr


class FeatureTable(object):

    def __init__(self, header_byte_length, arr):
        header_arr = arr[0:header_byte_length]
        self._header = FeatureTableHeader(header_arr)

        body_arr = arr[header_byte_length:]
        self._body = FeatureTableBody(self._header, body_arr)

    def npoints(self):
        return self._header.npoints

    def schema(self):
        return self._header.schema

    def point_arr(self, n):
        return self._body.point(n)

    def point(self, n):
        arr = self._body.point(n)
        return Point(self._header.schema, arr)
