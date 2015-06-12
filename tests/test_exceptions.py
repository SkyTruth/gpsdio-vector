"""
Make sure specific exceptions are raised.
"""


import pytest

import gpsdio_vector_driver.core


def test_bad_file_path(tmpdir):

    with pytest.raises(TypeError):
        gpsdio_vector_driver.core.Vector(None)
