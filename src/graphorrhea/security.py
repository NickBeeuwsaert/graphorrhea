import warnings
from datetime import datetime, timedelta

import jwt
from pyramid.authorization import ACLHelper
from pyramid.interfaces import ISecurityPolicy
from pyramid.security import Authenticated, Everyone


class InvalidAuthorizationError(Exception):
    pass


def _security_policy(request):
    return request.registry.queryUtility(ISecurityPolicy)


class SecurityPolicy:
    def __init__(self, private_key, algorithm="HS256"):
        self._private_key = private_key
        self._algorithm = algorithm

        self._acl_helper = ACLHelper()

    def claims(self, request):
        """
        Get the claims from the JWT.

        This is the same as the identity() method, with the only difference
        being that any exceptions from getting and decoding the JWT are passed
        to the user, instead of returning None
        """
        try:
            auth_type, token = request.authorization
        except TypeError:
            raise InvalidAuthorizationError("Missing Authorization Header")

        if auth_type != "Bearer":
            raise InvalidAuthorizationError("Wrong authentication type")

        return jwt.decode(token, self._private_key, [self._algorithm])

    def authenticated_userid(self, request):
        identity = self.identity(request)

        if identity is not None:
            return identity.get("sub")

        return None

    def effective_principals(self, request):
        principals = [Everyone]
        identity = self.identity(request)

        if identity is not None:
            principals += [Authenticated, identity["sub"]]

        return principals

    def remember(self, request):
        warnings.warn(
            "remember() has no effect, tokens must be returned from API.",
        )
        return []

    def forget(self, request):
        warnings.warn("forget() has no effect.")
        return []

    def identity(self, request):
        """Get the claims from the JWT."""
        try:
            return self.claims(request)
        except (InvalidAuthorizationError, jwt.InvalidTokenError):
            return None

    def permits(self, request, context, permission):
        return self._acl_helper.permits(
            context,
            self.effective_principals(request),
            permission,
        )

    def create_token(self, sub, expiration=None, **claims):
        iat = datetime.utcnow()
        payload = {**claims, "sub": sub, "iat": iat}

        if expiration is not None:
            payload["exp"] = iat + timedelta(seconds=expiration)

        return jwt.encode(payload, self._private_key, self._algorithm)


def create_jwt(request, *args, **kwargs):
    """
    Return a new JWT.

    In order for this function to work, you must have a security policy
    registered with the requests associate application.
    """
    policy = _security_policy(request)

    return policy.create_token(*args, **kwargs)


def jwt_claims(request):
    """
    Return the JWT claims for the provided request, or raise a JWT error.

    In order for this function to work, you must have a security policy
    registered with the requests associate application.
    """
    policy = _security_policy(request)

    return policy.claims(request)


def jwt_exception_view(request):
    """Error handler to handle any JWT-decoding related errors."""
    request.response.status_code = 401
    exception = request.exception
    (message,) = exception.args
    return {"message": message, "exception": type(exception).__name__}


def includeme(config):
    settings = config.registry.settings
    config.set_security_policy(SecurityPolicy(settings.pop("jwt.private_key")))

    config.add_request_method(jwt_claims, reify=True)
    config.add_request_method(create_jwt)
