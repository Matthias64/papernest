Papernest Coding Test
---------------------

The goal of the project is to answer the problem described
`here <https://docs.google.com/document/d/1sxNf2fC7rvhxmbd85t7O-oDv3OOJ21sH_QSfmZuIIb0/edit>`_
that is to build a small api project that we can request with a textual address request
and retrieve 2G/3G/4G network coverage for each operator (if available) in the response.

Quickstart
----------

This project uses a PostgreSQL database with POSTGIS extension for geographic coordinates.
You need to create one locally for it to work.

You can use conda to load all required python libraries from the file papernest_env.yaml ::

    conda env create --file papernest_env.yaml


Set environment variables ::

    set FLASK_APP=papernest.py
    set DATABASE_URL=postgres://postgres:password@localhost:5433

Then you can update your DB model using  ::

    flask db upgrade

And load DB with testing data ::

    python manage.py init_db_demo


To run the web application use::

    python papernest.py


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app`` and models.


Running Tests
-------------

Set the test DB environment variable  ::

    set FLASK_APP=papernest.py
    set DATABASE_URL_TEST=postgres://postgres:password@localhost:5433/papernesttest


To run all tests, run ::

    pytest


Network Coverage API
--------------------

You can now retrieve Network coverage information using the API below.::

    http://127.0.0.1:5000/api/network_coverage/<string:address>/<float:max_distance>

``<string:address>`` is an address string e.g. "42+rue+papernest+75011+Paris"
``<float:max_distance>`` is the maximum range in which you want to look for antennas (in meters).
If you don't specify it, max_distance used is 1km.
