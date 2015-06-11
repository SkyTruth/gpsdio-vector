====================
gpsdio vector driver
====================

.. image:: https://travis-ci.org/SkyTruth/gpsdio-vector-plugin.svg?branch=master
    :target: https://travis-ci.org/SkyTruth/gpsdio-vector-plugin


.. image:: https://coveralls.io/repos/SkyTruth/gpsdio-vector-plugin/badge.svg?branch=master
    :target: https://coveralls.io/r/SkyTruth/gpsdio-vector-plugin

A driver for gpsdio that enables writing to a `Fiona <https://github.com/Toblerity/Fiona>`_ supported `OGR <http://www.gdal.org/>`_ layer.


Installing
----------

Via pip:

.. code-block:: console

    $ pip install gpsdio-vector-driver

From master:

.. code-block:: console

    $ git clone https://github.com/SkyTruth/gpsdio-vector-driver
    $ cd gpsdio-vector-driver
    $ pip install .


Developing
----------

.. code-block::

    $ git clone https://github.com/SkyTruth/gpsdio-vector-driver
    $ cd gpsdio-vector-driver
    $ virtualenv venv && source venv/bin/activate
    $ pip install -e .[test]
    $ py.test tests --cov gpsdio_vector_driver --cov-report term-missing
