from pathlib import Path

import pytest
import webtest
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig

from graphorrhea import main


def pytest_addoption(parser):
    parser.addoption("--app-settings", action="store", metavar="SETTINGS_FILE")


@pytest.fixture(scope="session")
def app_settings(request):
    return get_appsettings(
        str(Path(request.config.option.app_settings or "testing.ini").resolve())
    )


@pytest.fixture(scope="session")
def app(app_settings):
    return main({}, **app_settings)


@pytest.fixture
def testapp(app):
    return webtest.TestApp(app)


@pytest.fixture
def app_request(app):
    with prepare(registry=app.registry) as environment:
        request = environment["request"]

        yield request


@pytest.fixture
def dummy_request():
    return DummyRequest()


def dummy_config(dummy_request):
    with testConfig(request=dummy_request):
        yield config
