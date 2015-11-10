# -*- coding: utf-8 -*-
import configparser
from sqlalchemy import (
    Column,
    String,
    Integer,
    create_engine,
    )
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    )
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

MainSession = scoped_session(sessionmaker())
SlaveSession = scoped_session(sessionmaker())
OtherSession = scoped_session(sessionmaker())

session_factories = {
    'master': MainSession,
    'slave': SlaveSession,
    'other': OtherSession,
    }


class MainTable(Base):
    __tablename__ = 'MainTable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    count = Column(Integer, default=0, nullable=False)


class OtherTable(Base):
    __tablename__ = 'OtherTable'

    id = Column(Integer, primary_key=True)
    name_other = Column(String)
    count_other = Column(Integer, default=0, nullable=False)


def get_db_url(ini_path):
    ini = configparser.SafeConfigParser()
    ini.read(ini_path)
    return ini['alembic']['sqlalchemy.url']


from zope.interface import (
    Interface,
    )
from zope.interface.registry import Components


class IDBSessionFactory(Interface):
    pass


def bind_engine(name, url=None, ini_path=None):
    if url is None:
        url = get_db_url(ini_path)
    engine = create_engine(url)
    session_factory = session_factories.get(name, None)
    if session_factory is None:
        raise ValueError
    session_factory.configure(bind=engine)
    return session_factory


def install_engine(registry, name, *args, **kwds):
    session_factory = bind_engine(name, *args, **kwds)
    registry.registerUtility(
        session_factory,
        IDBSessionFactory,
        name
        )


def bootstrap(registry):
    install_engine(registry, name='master', ini_path='migrations/master/alembic.ini')
    install_engine(registry, name='slave', url='sqlite:///slave.db')
    install_engine(registry, name='other', ini_path='migrations/other/alembic.ini')


def main():
    registry = Components()
    bootstrap(registry)

    session_factory = registry.queryUtility(IDBSessionFactory, 'master')
    session = session_factory()
    a = MainTable()
    a.name = 'test'
    session.add(a)
    print(session.get_bind())
    session.commit()

    session_factory = registry.queryUtility(IDBSessionFactory, 'other')
    session = session_factory()
    a = OtherTable()
    a.name_other = 'test'
    session.add(a)
    print(session.get_bind())
    session.commit()


if __name__ == '__main__':
    main()
