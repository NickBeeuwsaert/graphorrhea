from graphorrhea.views import index


def test_index(dummy_request):
    assert index(dummy_request) == "Hello, world!"
