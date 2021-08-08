===========
Graphorrhea
===========
A note taking app, using git as a database, so you can own your notes with you anywhere.

Prerequisites
-------------

Poetry_ is used for package management and venv management on the backend, while NPM_/Snowpack_ is used on the frontend.

These are some optional dependencies:

pyenv_
    For python version management

Quickstart
----------
To create the user database (users are not stored in git)::

    poetry run alembic upgrade head

Then, to run the API server::

    poetry run pserve development.toml

And to run the frontend::

    # (In a separate terminal)
    npm i
    npm run start

Snowpack_ will open up a new browser window, if it doesn't point your browser at ``http://127.0.0.1:8080``.

Then go hog-wild.


Roadmap
-------

* UI has yet to reach it's final form. Right now its mostly just placeholder.
* Rip and tear the CSS modules stuff into BEM.
* Adding more unit tests, they fell by the wayside during development while I stabilized the API.
* Remove Snowpack dependency, and try to use plain ESM imports because I am insane.
* Iron out OpenAPI document
* Add unicorns



.. _Poetry: https://python-poetry.org/
.. _pyenv: https://github.com/pyenv/pyenv
.. _NPM: https://www.npmjs.com/
.. _Snowpack: https://www.snowpack.dev/