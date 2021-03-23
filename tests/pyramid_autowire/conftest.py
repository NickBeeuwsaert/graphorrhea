import pytest
from pyramid_autowire import ViewMapper


@pytest.fixture
def view_mapper():
    return ViewMapper(attr="view")
