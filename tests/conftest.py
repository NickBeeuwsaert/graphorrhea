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
def settings_file(request):
    return str(Path(request.config.option.app_settings or "testing.toml").resolve())


@pytest.fixture(scope="session")
def settings(settings_file):
    return get_appsettings(settings_file)


@pytest.fixture(scope="session")
def app(settings):
    return main({}, **settings)


@pytest.fixture
def testapp(app):
    return webtest.TestApp(app)


@pytest.fixture
def dummy_request():
    return DummyRequest()


def dummy_config(dummy_request):
    with testConfig(request=dummy_request):
        yield config
