from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
_engine = None
_db_factory = None

db_session = scoped_session(lambda: _db_factory())


def init_engine(db_url: str):
    global _engine, _db_factory
    _engine = create_engine(db_url, pool_pre_ping=True)
    _db_factory = sessionmaker(bind=_engine, autocommit=False, autoflush=False)


def get_engine():
    return _engine

