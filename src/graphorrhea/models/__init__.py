"""Database models."""
from pyramid.interfaces import IRequest
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register

from ..interfaces import IDatabaseSession
from .user import User

__all__ = ("User",)


def includeme(config):
    settings = config.get_settings()

    engine = engine_from_config(settings, future=True)

    session_factory = sessionmaker(engine)
    config.registry["dbsession_factory"] = session_factory

    def dbsession(request):
        print("New session")
        dbsession = session_factory(info={"request": request})
        # For pshell
        dbsession.__doc__ = "Database session."
        register(dbsession, transaction_manager=request.tm)
        return dbsession

    config.add_request_method(dbsession, reify=True)
    config.registry.registerAdapter(dbsession, (IRequest,), IDatabaseSession)
