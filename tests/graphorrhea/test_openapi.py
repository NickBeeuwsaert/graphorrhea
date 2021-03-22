from unittest.mock import ANY

import pytest

from graphorrhea.openapi import views


class TestDirectoryEndpoint:
    # Not sure if this tests have value
    # since they are mostly testing the behavior of
    # pyramid_openapi3. But knowing the view won't get
    # bunk data is nice so meh

    @pytest.mark.parametrize(
        "path",
        [
            "test",
            "/.",
            "/.invalid",
            "/..",
            "/test/.invalid",
        ],
    )
    def test_rejects_invalid_path(self, api_test_app, path):
        response = api_test_app.get("/api/v1/directory", {"path": path}, status=400)
        assert {"message": ANY, "exception": "ValidationError"} in response.json

    def test_rejects_empty_path(self, api_test_app):
        response = api_test_app.get(f"/api/v1/directory", {"path": ""}, status=400)
        assert {
            "message": ANY,
            "field": "path",
            "exception": "EmptyParameterValue",
        } in response.json

    def test_rejects_missing_path(self, api_test_app):
        response = api_test_app.get("/api/v1/directory", status=400)
        assert {
            "message": ANY,
            "field": "path",
            "exception": "MissingRequiredParameter",
        } in response.json
