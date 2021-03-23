import pytest

from pyramid_di import ViewMapper


@pytest.fixture
def view_mapper():
    return ViewMapper(attr="view")
