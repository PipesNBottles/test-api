import contextlib
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

DEFAULT_URI = "sqlite:///local.db"


def _create_uri(name, driver, host, username, password):
    database = name or os.environ["DATABASE_NAME"]
    driver = driver or os.environ["DATABASE_DRIVER"]
    host = host or os.environ.get("DATABASE_HOST", "db")
    username = username or os.environ["DATABASE_USERNAME"]
    password = password or os.environ["DATABASE_PASSWORD"]
    return f"{driver}://{username}:{password}@{host}/{database}"


def create_uri(default=DEFAULT_URI, raise_exception=False, **kwargs):
    database = kwargs.get("name")
    driver = kwargs.get("driver", "postgresql+psycopg2")
    host = kwargs.get("host")
    username = kwargs.get("username")
    password = kwargs.get("password")
    uri = None

    with contextlib.suppress(Exception):
        uri = _create_uri(database, driver, host, username, password)

    if uri is None and raise_exception:
        raise ValueError("Unable to create database uri")

    return uri or default or DEFAULT_URI


def setup(uri=None, connection_args=None, create_all=False, base=None, **kwargs):
    """
    Initializes all tables for the database engine
    """

    uri = uri or DEFAULT_URI
    if uri.startswith("sqlite"):
        create_all = True
        kwargs = {}
        connection_args = dict(check_same_thread=False)

    engine = create_engine(uri, connect_args=connection_args or {}, **kwargs)
    if create_all and base:
        base.metadata.create_all(bind=engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, session


def cleanup(engine, base):
    """
    drops all tables from the database engine
    """
    base.metadata.drop_all(bind=engine)
    if os.path.isfile("local.db"):
        os.remove("local.db")


__all__ = ["Base", "create_uri", "cleanup", "setup"]
