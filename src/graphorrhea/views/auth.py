from pyramid.httpexceptions import (
    HTTPBadRequest,
    HTTPForbidden,
    HTTPNotFound,
    HTTPUnauthorized,
)
from pyramid.view import view_config

from graphorrhea.models.user import User

# TODO: move this out into the config file,
# and access it from the SecurityPolicy
TOKEN_EXPIRATION = 60 * 60  # 60 minutes


@view_config(
    route_name="auth.login",
    request_method="POST",
    renderer="json",
    openapi=True,
)
def login(request):
    payload = request.json
    dbsession = request.dbsession

    try:
        username = payload["username"]
        password = payload["password"]
    except KeyError:
        raise HTTPBadRequest(headers={"content_type": "application/json"})

    user = dbsession.query(User).filter(User.username == username).first()

    if not (user and user.password == password):
        raise HTTPForbidden()

    return dict(
        token=request.create_jwt(user.username, expiration=TOKEN_EXPIRATION),
        refresh_token="",
    )


@view_config(
    route_name="auth.renew",
    request_method="POST",
    renderer="json",
    openapi=True,
)
def renew(request):
    """
    Given a valid JWT, Renew it.

    This API should probably implement a token pair, with a access token being
    short lived and it's corresponding refresh token being long lived. But then
    I'd have to implement some way to expire refresh tokens, which would
    probably involve tracking them in a database, so if an earlier token
    is compromised all subsequent tokens will be rejected by default.

    Quick overview of what this will look like:

    There should be a database table with a schema similar to this::

        CREATE TABLE refresh_tokens (
            id SERIAL PRIMARY KEY,
            -- Make unique so token reuse won't work
            -- Additionally, (and this should neer happen) set up a cascade
            -- So that if a token from a different lineage ever references
            -- a token marked for deletion, it will get removed as well
            parent_id INTEGER UNIQUE ON DELETE CASCADE,
            token TEXT NOT NULL, -- Probably a JWT just to track the ID
                                 -- plus exp, would save a DB call if
                                 -- the token is expired
            expires_at DATETIME NOT NULL -- For cleaning out the database of
                                         -- expired refresh tokens
        );

    If, when inserting a new token a integrity error occurs because of the
    unique index on `parent_id`, we can invalidate the entire token lineage
    with the following CTE (it might also be useful to log the potential
    token leak)::

        WITH RECURSIVE
            token_lineage(id, parent_id) AS (
                SELECT id, parent_id FROM refresh_tokens WHERE id = ?
                UNION ALL
                SELECT
                    lineage.id, lineage.parent_id
                FROM lineage
                JOIN refresh_token AS token ON (tokens.id = lineage.parent_id)
            )
            DELETE FROM
                refresh_tokens
            USING token_lineage
            WpassHERE token_lineage.id = refresh_tokens.id;

    I do need to do more research on refresh tokens to make sure I do fully
    understand it, this is just some quick notes I've jotted down for future
    reference.
    """
    return dict(
        token=request.create_jwt(
            expiration=TOKEN_EXPIRATION,
            **request.jwt_claims,
        )
    )


@view_config(
    route_name="auth.register",
    request_method="POST",
    renderer="json",
    openapi=True,
)
def registera(request):
    """
    Register a user.
    """
    dbsession = request.dbsession
    json = request.json

    try:
        username = json["username"]
        password = json["password"]
    except KeyError:
        raise HTTPBadRequest

    user = User(username=username, password=password)

    dbsession.add(user)
    dbsession.flush()

    return dict(
        username=user.username,
        id=user.id,
    )
