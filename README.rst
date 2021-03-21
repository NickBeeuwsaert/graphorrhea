===========
Graphorrhea
===========
A note taking app.

Prerequisites
-------------

Poetry_ is used for package management and venv management.

These are some optional dependencies:

pyenv_
    For python version management

Docker_ & docker-compose_ or Podman_ & podman-compose_
    For running the application in a container

Quickstart
----------

If you are on a platform that supports Docker_/Podman_, you should be able to just do the following:

.. code-block:: sh

    # Install the application locally (for migrations)
    poetry install
    # Start postgres, elasticsearch, redis and graphorrhea
    docker-compose up

    # (separate terminal)
    poetry run alembic upgrade head

Manual Setup
------------

Set up the following services:

* ElasticSearch_
* Redis_
* Postgres_ (Or just use SQLite)

Configure development.ini to point to the above services.

.. code-block:: sh

    poetry run pserve --reload development.ini

Unit Testing
------------
.. code-block:: sh

    poetry run pytest

.. _Poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _Docker: https://www.docker.com/get-started
.. _docker-compose: https://docs.docker.com/compose/install/
.. _Podman: https://podman.io/getting-started/installation
.. _podman-compose: https://github.com/containers/podman-compose
.. _Postgres: https://www.postgresql.org/download/
.. _Redis: https://redis.io/
.. _ElasticSearch: https://www.elastic.co/start