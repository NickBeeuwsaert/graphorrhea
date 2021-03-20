import sqlalchemy as sa

from ._meta import mapped
from .types import PasswordType


@mapped
class User:
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.Text, unique=True, nullable=False)
    password = sa.Column(
        PasswordType(
            schemes=["pbkdf2_sha256"],
            deprecated="auto",
        )
    )
