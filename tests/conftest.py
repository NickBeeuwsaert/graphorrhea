from pathlib import Path

import pytest
import webtest
from pyramid.paster import get_appsettings
from pyramid.scripting import prepare
from pyramid.testing import DummyRequest, testConfig

from graphorrhea import api, frontend, main


def pytest_addoption(parser):
    parser.addoption("--app-settings", action="store", metavar="SETTINGS_FILE")


@pytest.fixture(scope="session")
def settings_file(request):
    return str(Path(request.config.option.app_settings or "testing.toml").resolve())


@pytest.fixture(scope="session")
def frontend_settings(settings_file):
    return get_appsettings(settings_file, "frontend")


@pytest.fixture(scope="session")
def api_settings(settings_file):
    return get_appsettings(settings_file, "api")


@pytest.fixture(scope="session")
def frontend_app(frontend_settings):
    return frontend({}, **frontend_settings)


@pytest.fixture(scope="session")
def api_app(api_settings):
    return api({}, **api_settings)


@pytest.fixture
def frontend_test_app(frontend_app):
    return webtest.TestApp(frontend_app)


@pytest.fixture
def api_test_app(api_app):
    return webtest.TestApp(api_app)


@pytest.fixture
def frontend_request(frontend_app):
    with prepare(registry=frontend_app.registry) as environment:
        request = environment["request"]

        yield request


@pytest.fixture
def api_request(api_app):
    with prepare(registry=api_app.registry) as environment:
        request = environment["request"]

        yield request


@pytest.fixture
def dummy_request():
    return DummyRequest()


def dummy_config(dummy_request):
    with testConfig(request=dummy_request):
        yield config
