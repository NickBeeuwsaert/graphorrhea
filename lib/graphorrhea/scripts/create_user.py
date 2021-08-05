import argparse
import getpass

from pyramid.paster import bootstrap

from graphorrhea.models import User

parser = argparse.ArgumentParser()
parser.add_argument("config_uri", metavar="CONFIG", type=str)
parser.add_argument("-u", "--username", metavar="USERNAME", type=str, default="")
parser.add_argument("-p", "--password", metavar="PASSWORD", type=str, default="")


def main():
    """
    Create a user in the database.

    Since registration won't be available in the app, we create users while setting
    the app up.
    """
    args = parser.parse_args()

    username = args.username
    password = args.password
    if username is None:
        default_username = getpass.getuser()
        username = (
            input(f"Username (leave empty for {default_username}): ")
            or default_username
        )

    while not password:
        password = input("Password: ")

    with bootstrap(args.config_uri) as env:
        registry = env["registry"]
        dbsession_factory = registry["dbsession_factory"]

        with dbsession_factory.begin() as session:
            session.add(User(username=username, password=password))
