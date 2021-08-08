from zope.interface import Interface


class IGitResource(Interface):
    pass


class IDatabaseSession(Interface):
    """Marker class for SQLAlchemy database sessions."""
