from graphorrhea.views import index


def test_index(frontend_request):
    assert index(frontend_request) == "Hello, world!"
