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
    ini = configparser.SafeCOnfigParser()
    ini.read(ini_path)
    return ini['alembic']['sqlalchemy.uri']


def bootstrap():
    master = create_engine('sqlite:///master.db')
    slave = create_engine('sqlite:///slave.db')
    other = create_engine('sqlite:///other.db')

    MainSession.configure(bind=master)
    SlaveSession.configure(bind=slave)
    OtherSession.configure(bind=other)


def main():
    bootstrap()

    session = MainSession()
    a = MainTable()
    a.name = 'test'
    session.add(a)
    print(session.get_bind())
    session.commit()

    session = OtherSession()
    a = OtherTable()
    a.name_other = 'test'
    session.add(a)
    print(session.get_bind())
    session.commit()


if __name__ == '__main__':
    main()
