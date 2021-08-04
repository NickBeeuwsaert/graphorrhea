from datetime import datetime, timedelta

import jwt
import pytest
from pyramid.interfaces import ISecurityPolicy
from pyramid.testing import DummyRequest

from graphorrhea.security import SecurityPolicy, create_jwt, jwt_claims


@pytest.fixture
def private_key(request):
    return "DUMMY KEY"


@pytest.fixture
def security_policy(private_key, dummy_request):
    return SecurityPolicy(private_key)


@pytest.mark.parametrize(
    ("claims", "key", "expected_error"),
    [
        pytest.param(
            {"exp": datetime.utcnow() - timedelta(seconds=3600)},
            None,
            jwt.ExpiredSignatureError,
            id="Expired token",
        ),
        pytest.param(
            {}, "INVALID", jwt.InvalidSignatureError, id="Token with invalid key "
        ),
    ],
)
def test_security_policy_raises_on_error(
    dummy_request, private_key, security_policy, claims, key, expected_error
):
    expiration = timedelta(seconds=30)
    iat = datetime.utcnow()
    exp = iat + expiration

    dummy_request.registry.registerUtility(security_policy, ISecurityPolicy)

    token = jwt.encode(
        {"iat": iat, "exp": exp, "sub": "test_principal", **claims}, key or private_key
    )
    dummy_request.authorization = ("Bearer", token)

    with pytest.raises(expected_error):
        jwt_claims(dummy_request)
    with pytest.raises(expected_error):
        security_policy.claims(dummy_request)


@pytest.mark.parametrize(
    ("claims", "key", "expected_value"),
    [
        pytest.param(
            {"exp": datetime.utcnow() - timedelta(seconds=3600), "sub": "sub"},
            None,
            "sub",
            id="Expired token",
        ),
        pytest.param({}, "INVALID", None, id="Token with invalid key"),
        pytest.param({}, None, None, id="Token with no sub key"),
    ],
)
def test_authenticated_userid_returns_none_or_sub(
    dummy_request, private_key, security_policy, claims, key, expected_value
):
    token = jwt.encode(claims, key or private_key)

    dummy_request.authorization = ("Bearer", token)

    security_policy.authenticated_userid(dummy_request) == expected_value


def test_identity_returns_claims(dummy_request, security_policy, private_key):
    claims = {"data": "test"}

    dummy_request.authorization = ("Bearer", jwt.encode(claims, private_key))

    assert security_policy.identity(dummy_request) == claims


def test_remember_warns(dummy_request, security_policy):
    with pytest.warns(UserWarning):
        assert security_policy.remember(dummy_request) == []


def test_forget_warns(dummy_request, security_policy):
    with pytest.warns(UserWarning):
        assert security_policy.forget(dummy_request) == []


def test_create_token_uses_private_key(dummy_request, security_policy, private_key):
    dummy_request.registry.registerUtility(security_policy, ISecurityPolicy)
    sub = "test_sub"
    token = security_policy.create_token(sub)
    assert jwt.decode(token, private_key, algorithms=["HS256"])["sub"] == sub

    token = create_jwt(dummy_request, sub)
    assert jwt.decode(token, private_key, algorithms=["HS256"])["sub"] == sub
