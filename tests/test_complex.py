"""
More complex tests
"""


from click.testing import CliRunner
import fiona as fio
import gpsdio.cli.main

from gpsdio_vector_driver.core import Vector


def test_additional_fields(tmpdir):

    p = tmpdir.mkdir('testfiles')
    testfile = str(p.join('out.shp'))

    result = CliRunner().invoke(gpsdio.cli.main.main_group, [
        '--o-drv', 'Vector',
        '--o-drv-opt', 'driver=ESRI Shapefile',
        '--o-drv-opt', 'fields=new_field:str:40,oth_n_fld:float:25.1',
        'etl',
        'tests/data/points.json',
        testfile
    ])
    assert result.exit_code == 0

    with fio.open(testfile) as src:
        for f in list(Vector.default_fields) + ['new_field', 'oth_n_fld']:
            assert f in src.schema['properties']

        assert 'str' in src.schema['properties']['new_field']
        assert 'float' in src.schema['properties']['oth_n_fld']


def test_complex_via_api(tmpdir):

    # Make sure we can give `fields` as a dict and `driver` via the API.

    p = tmpdir.mkdir('testfiles')
    testfile = str(p.join('out.geojson'))

    do = {
        'fields': {
            'new_field': 'str'
        },
        'driver': 'GeoJSON'
    }

    with gpsdio.open('tests/data/points.json') as src:
        with gpsdio.open(testfile, 'w', driver='Vector', do=do) as dst:
            for idx, msg in enumerate(src):
                dst.write(msg)

    num_msgs = idx + 1

    with fio.open(testfile) as src:
        assert src.driver == 'GeoJSON'
        assert 'str' in src.schema['properties']['new_field']
        assert num_msgs == len(src)
