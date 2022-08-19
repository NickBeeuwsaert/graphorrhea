===========
Graphorrhea
===========
A note taking app, using git as a database, so you can own your notes with you anywhere.

Prerequisites
-------------

PDM_ is used for package management and venv management on the backend, while NPM_/ESBuild_ is used on the frontend.

These are some optional dependencies:

pyenv_
    For python version management

Quickstart
----------
To create the user database (users are not stored in git)::

    pdm run alembic upgrade head

Then, to run the API server::

    poetry run pserve development.toml

And to run the frontend::

    # (In a separate terminal)
    npm i
    npm run start

ESBuild_ will start serving the frontend, point your browser to ``http://127.0.0.1:8080``.

Then go hog-wild.


Roadmap
-------

* UI has yet to reach it's final form. Right now its mostly just placeholder.
* Rip and tear the CSS stuff into BEM.
* Adding more unit tests, they fell by the wayside during development while I stabilized the API.
* Iron out OpenAPI document
* Add unicorns
* Swap AcidFS out for a custom git wrapper. AcidFS is nice, but it is subcommand based. It would be better to have an abstraction based on pygit2, that integrates better with pyramids traversal.



.. _PDM: https://pdm.fming.dev/latest/
.. _pyenv: https://github.com/pyenv/pyenv
.. _NPM: https://www.npmjs.com/
.. _ESBuild: https://esbuild.github.io/