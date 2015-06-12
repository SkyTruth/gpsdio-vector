"""
Ensure that the standard use-cases are operating properly.
"""


from click.testing import CliRunner
import fiona as fio
import gpsdio.drivers
import gpsdio.cli.main

from gpsdio_vector_driver.core import Vector


def test_register():
    # Make sure the driver is actually registering
    assert Vector == gpsdio.drivers.BaseDriver.by_name[Vector.driver_name]


def test_defaults(tmpdir):

    testfile = str(tmpdir.mkdir('out').join('out.shp'))
    result = CliRunner().invoke(gpsdio.cli.main.main_group, [
        '--o-drv', 'Vector',
        'etl',
        'tests/data/points.json',
        testfile
    ])
    assert result.exit_code == 0

    with gpsdio.open('tests/data/points.json') as src, fio.open(testfile) as vector:

        messages = list(src)
        assert vector.driver == 'ESRI Shapefile'
        assert len(vector) == len(messages)

        # Check coordinates - properties/fields are validated in another
        # more complex test
        for msg, feat in zip(messages, vector):

            e_x = msg['lon']
            e_y = msg['lat']
            a_x, a_y = feat['geometry']['coordinates'][:2]
            assert round(e_x, 7) == round(a_x, 7)
            assert round(e_y, 7) == round(a_y, 7)


def test_different_driver(tmpdir):

    testfile = str(tmpdir.mkdir('out').join('out.geojson'))
    result = CliRunner().invoke(gpsdio.cli.main.main_group, [
        '--o-drv', 'Vector',
        '--o-drv-opt', 'driver=GeoJSON',
        'etl',
        'tests/data/points.json',
        testfile
    ])
    assert result.exit_code == 0

    with gpsdio.open('tests/data/points.json') as src, fio.open(testfile) as actual:
        assert len(actual) == len(list(src))
        assert actual.driver == 'GeoJSON'
