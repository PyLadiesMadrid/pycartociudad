=============
pycartociudad
=============

.. image:: https://raw.githubusercontent.com/PyLadiesMadrid/pycartociudad/4e7043531bfae74ed2b96a5ce66d5d4a07a2dd01/docs/pycartociudad.svg



.. image:: https://img.shields.io/pypi/v/pycartociudad.svg
        :target: https://pypi.python.org/pypi/pycartociudad

.. image:: https://img.shields.io/travis/pyladiesmadrid/pycartociudad.svg
        :target: https://travis-ci.com/pyladiesmadrid/pycartociudad

.. image:: https://readthedocs.org/projects/pycartociudad/badge/?version=latest
        :target: https://pycartociudad.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



pycartociudad contains Python functions to access the CartoCiudad REST and WPS API (REST y WPS) from IGN with spanish cartography services.


Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Prerequisites
~~~~~~~~~~~~~

To use the pycartociudad package you will need to have python installed (at least version 3.8). For detailed instructions, please check the `Downloading Python guide`_

.. _`Downloading Python guide`: https://wiki.python.org/moin/BeginnersGuide/Download

Dependencies can be managed through a pipenv wrapper. In order to install pipenv, check the `pipenv installation documentation`_.

.. _`pipenv installation documentation`: https://pipenv.pypa.io/en/latest/#install-pipenv-today


Installing
~~~~~~~~~~

To install the latest published PyPI version of pycartociudad::

	pip install pycartociudad

To upgrade an already installed ``pycartociudad`` package from PyPI::

	pip install --upgrade pycartociudad


The ``pycartociudad`` development repository can be found in the `pycartociudad GitHub repository`_. To make a local copy of the ``pycartociudad`` repository, clone it or download is as a zip file.

.. _`pycartociudad GitHub repository`: https://github.com/PyLadiesMadrid/pycartociudad

To get a development env running, go to the downloaded or cloned ``pycartociudad`` folder and install it using pipenv::

    $ pipenv install


Running the tests
-----------------

To run a subset of tests::

    $ python -m unittest tests.test_geocode
    $ python -m unittest tests.test_reverse_geocode


Deployment
----------

TO-DO


Built with
----------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


Documentation
-------------

The ``pycartociudad`` documentation can be found in `pycartociudad readthedocs`_.

.. _`pycartociudad readthedocs`: https://pycartociudad.readthedocs.io

Details on the API implementation can be found in the official `Cartociudad API specs`_.

.. _`Cartociudad API specs`: https://www.cartociudad.es/recursos/Documentacion_tecnica/CARTOCIUDAD_ServiciosWeb.pdf

Contributing
------------
Please read `CONTRIBUTING.rst`_ for the process of submitting pull requests to us.

.. _`CONTRIBUTING.rst`: https://github.com/PyLadiesMadrid/pycartociudad/blob/main/CONTRIBUTING.rst

For details on our code of conduct, check the `PyLadies Code of Conduct`_.

.. _`PyLadies Code of Conduct`: https://madrid.pyladies.com/coc/

Features
--------

Geocoding
~~~~~~~~~
Geocoding is the geolocation of addresses in Spain via Cartociudad API calls. Calling the ``geocode`` function returns the details of the closest address in Spain to the indicated address.

>>> import pycartociudad as pycc
>>> pycc.geocode('Plaza mayor 1, madrid')    
{'id': '280790001063', 'province': 'Madrid', 'comunidadAutonoma': 'Comunidad de Madrid', 'muni': 'Madrid', 'type': 'portal', 'address': 'MAYOR', 'postalCode': '28012', 'poblacion': 'Madrid', 'geom': 'POINT (-3.7066353973101624 40.41505683353346)', 'tip_via': 'PLAZA', 'lat': 40.41505683353346, 'lng': -3.7066353973101624, 'portalNumber': 1, 'stateMsg': 'Resultado exacto de la bÃºsqueda', 'state': 1, 'countryCode': '011', 'refCatastral': None}


Reverse geocoding
~~~~~~~~~~~~~~~~~

Reverse geocoding is the search of an address details based on latitude and longitude coordinates.

>>> import pycartociudad as pycc
>>> pycc.reverse_geocode(40.4472476241486,-3.7076498426208833)
{'id': '280790165933', 'province': 'Madrid', 'comunidadAutonoma': 'Comunidad de Madrid', 'muni': 'Madrid', 'type': None, 'address': 'REINA VICTORIA', 'postalCode': '28003', 'poblacion': 'Madrid', 'geom': 'POINT (-3.707649842620833 40.447247624136764)', 'tip_via': 'AVENIDA', 'lat': 40.447247624136764, 'lng': -3.707649842620833, 'portalNumber': 22, 'stateMsg': 'Resultado exacto de la bÃºsqueda', 'state': 1, 'priority': 0, 'countryCode': '011', 'refCatastral': None}


Reverse geocoding can be performed to look for cadastral details with the cadastral parameter

>>> pycc.reverse_geocode(40.4472476241486,-3.7076498426208833, cadastral=True)
{'id': None, 'province': None, 'comunidadAutonoma': None, 'muni': None, 'type': None, 'address': '0079609VK4707G', 'postalCode': None, 'poblacion': None, 'geom': 'POINT (-3.7076498426208833 40.4472476241486)', 'tip_via': None, 'lat': 40.4472476241486, 'lng': -3.7076498426208833, 'portalNumber': 0, 'stateMsg': 'Resultado exacto de la bÃºsqueda', 'state': 1, 'priority': 0, 'countryCode': '011', 'refCatastral': 'AV REINA VICTORIA 22 MADRID (MADRID)'}


Get location info
~~~~~~~~~~~~~~~~~

The ``get_location_info`` function gets extra information of a location using official spanish web map services, such as cadastre, census or geocoding information.

>>> import pycartociudad as pycc
>>> pycc.get_location_info(40.4472476241486,-3.7076498426208833)
{'cadastral_ref': '0079609VK4707G', 'census_section': '2807906001', 'district_code': '2807906', 'id': '280790165933', 'province': 'Madrid', 'comunidadAutonoma': 'Comunidad de Madrid', 'muni': 'Madrid', 'type': None, 'address': 'REINA VICTORIA', 'postalCode': '28003', 'poblacion': 'Madrid', 'geom': 'POINT (-3.707649842620833 40.447247624136764)', 'tip_via': 'AVENIDA', 'lat': 40.447247624136764, 'lng': -3.707649842620833, 'portalNumber': 22, 'stateMsg': 'Resultado exacto de la bÃºsqueda', 'state': 1, 'priority': 0, 'countryCode': '011', 'refCatastral': None}


Route between two points
~~~~~~~~~~~~~~~~~~~~~~~~

This function gets the route between two points (encoded with their latitude-longitude coordinates), either walking or in a vehicle.

>>> import pycartociudad as pycc
>>> d = pycc.route_between_two_points(40.447313139920475,-3.704361232340851,40.44204376380937,-3.699671450323607)
>>> for i in d['instructionsData']['instruction']:
... 	print(i['description'])
... 
Continúe por GLORIETA CUATRO CAMINOS
Gire justo a la derecha por CALLE SANTA ENGRACIA
Gire a la izquierda por CALLE RIOS ROSAS
Objetivo logrado


Authors
-------
* **Luz Frías** - *Team Lead & Initial work* - `@koldLight`_.
* **Isabel González** - *Initial work* - `@zupeiza`_.
* **Beatriz Gómez** - *Initial work* - `@beatrizgoa`_.
* **Alicia Pérez** - *Initial work* - `@aliciapj`_.

.. _@koldLight: https://github.com/koldLight
.. _@zupeiza: https://github.com/zupeiza
.. _@beatrizgoa: https://github.com/beatrizgoa
.. _@aliciapj: https://github.com/aliciapj

For a list of contributors, check the `PyLadies pycartociudad contributor list`_

.. _`PyLadies pycartociudad contributor list`: https://github.com/PyLadiesMadrid/pycartociudad/graphs/contributors


License
-------

* Free software: CC-BY 4.0 scne.es

The data returned by this package is provided by IGN web services and implies the user's acceptance of a CC-BY 4.0 scne.es license. More info available in the `IGN license specs`_.

.. _`IGN license specs`: http://www.ign.es/web/resources/docs/IGNCnig/FOOT-Condiciones_Uso_eng.pdf
