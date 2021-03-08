from graphorrhea.views import index


def test_index(app_request):
    assert index(app_request) == "Hello, world!"
