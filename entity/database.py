import os
import sys
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from chargeEquipment import ChargeEquipment, Base as ChargeEquipmentBase
from sample import Sample, Base as SampleBase
from sampleStatistical import SampleStatistical, Base as SampleStatisticalBase

from sqlalchemy.orm import sessionmaker


class Database(object):

    def __init__(self):
        self.sqlite = 'sqlite:///tenergy.db'
        self.engine = create_engine(self.sqlite, echo=False)

    def drop(self):
        ChargeEquipment.__table__.drop(self.engine)
        Sample.__table__.drop(self.engine)
        SampleStatistical.__table__.drop(self.engine)

    def create(self):
        ChargeEquipmentBase.metadata.create_all(self.engine)
        SampleBase.metadata.create_all(self.engine)
        SampleStatisticalBase.metadata.create_all(self.engine)

    def create_session(self):
        session = sessionmaker(bind=self.engine)
        self.db_session = session()
        return self.db_session

    def find(self, clazz, where=None):
        session = self.create_session()
        query = session.query(clazz)
        if where is not None:
            query = query.filter(where)
        return query.all()

    def save(self, entity):
        session = self.create_session()
        session.add(entity)
        session.commit()
