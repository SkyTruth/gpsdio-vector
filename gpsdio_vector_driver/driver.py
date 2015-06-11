"""
Vector driver implementation
"""


from collections import OrderedDict
from copy import deepcopy

import fiona as fio
from gpsdio.drivers import BaseDriver
import six


class Vector(BaseDriver):

    """
    Write positional messages to a vector file.

    The fields listed below are included by default others may be added with
    the appropriate driver option.  Fields must include a definition as
    `name:type:width.precision`.  The minimum required definition is `name:type`.

        mmsi:int:30
        timestamp:str:40
        course:float:12.1
        speed:float:10.1
        heading:int:7

    Uses Fiona: https://github.com/Toblerity/Fiona


    Driver Options
    --------------
    crs : str or dict, optional
        Coordinate reference system to apply to output file.  No transforms
        are performed.  See Fiona's docs for more info.  (default: EPSG:4326)

    driver : str
        Name of OGR driver for output file. (default: ESRI Shapefile)

    line_file : str, optional
        Create a second output file that contains a single line for all points
        processed points.  Uses the same format as `driver`.  If omitted the
        line file is not created.

    fields : list or dict or str, optional
        Defaults to the list above.  Several syntaxes are supported:
            dict - Formatted like a Fiona schema with
                   `{'name': 'type:width.precision'}`
            list - Each element is `name:type:width.precision`.
            str - Same as list but with a comma between each definition.
    """

    io_modes = 'w',
    driver_name = 'vector'
    extensions = ('shp', 'geojson')

    def __init__(self, f, mode='w', driver='ESRI Shapefile', line=None,
                 crs='EPSG:4326', fields=None):

        properties = OrderedDict((
            ('mmsi', 'int:30'),
            ('timestamp', 'str:40'),
            ('course', 'float:12.1'),
            ('speed', 'float:10.1'),
            ('heading', 'int:7')
        ))

        if isinstance(fields, six.string_types):
            fields = fields.split(',')

        if isinstance(fields, (OrderedDict, dict)):
            properties.update(**fields)
        elif isinstance(fields, (list, tuple)):
            for d in fields:
                name, definition = d.split(':', 1)
                properties[name] = definition

        meta = {
            'schema': {
                'properties': properties,
                'geometry': 'Point'
            },
            'crs': crs,
            'driver': driver
        }

        BaseDriver.__init__(
            self,
            fio.open(f, mode, **meta)
        )

        # These objects are for writing the line file
        self._line_coords = []
        self._line = line
        self._line_meta = deepcopy(meta)
        self._line_meta['schema']['properties'] = {}
        self._line_meta['schema']['geometry'] = 'LineString'

    def write(self, msg):
        x = msg.get('lon')
        y = msg.get('lat')
        if x is not None and y is not None:
            self.stream.write({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': (x, y)
                },
                'properties': {f: msg.get(f) for f in self.stream.meta['schema']['properties']}
            })
        if self._line:
            self._line_coords.append((x, y))

    def close(self):
        self.stream.close()
        if self._line:
            with fio.open(self._line, 'w', **self._line_meta) as dst:
                dst.write({
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': self._line_coords
                    }
                })
        self._line_coords = []
