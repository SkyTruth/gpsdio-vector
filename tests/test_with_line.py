"""
Make sure the optional line file is written and has the expected characteristics.
"""


from click.testing import CliRunner
import fiona as fio
import gpsdio.cli.main


def test_with_line(tmpdir):

    p = tmpdir.mkdir('testfiles')
    testfile = str(p.join('out.geojson'))
    linefile = testfile.replace('out', 'line')

    result = CliRunner().invoke(gpsdio.cli.main.main_group, [
        '--o-drv', 'Vector',
        '--o-drv-opt', 'driver=GeoJSON',
        '--o-drv-opt', 'line={}'.format(linefile),
        'etl',
        'tests/data/points.json',
        testfile
    ])
    assert result.exit_code == 0

    with fio.open(linefile) as src:
        assert src.driver == 'GeoJSON'
        assert len(src) == 1
        assert src.schema['geometry'] == 'LineString'
        assert src.schema['properties'] == {}
        line_coordinates = src[0]['geometry']['coordinates']

    with fio.open(testfile) as vector, gpsdio.open('tests/data/points.json') as messages:
        for feature, msg, l_coord in zip(vector, messages, line_coordinates):
            m_x = msg['lon']
            m_y = msg['lat']
            f_x, f_y = feature['geometry']['coordinates'][:2]
            l_x, l_y = l_coord

            assert round(m_x, 7) == round(f_x, 7) == round(l_x, 7)
            assert round(m_y, 7) == round(f_y, 7) == round(l_y, 7)
