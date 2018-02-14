import os
import sys
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from chargeEquipment import ChargeEquipment, Base as ChargeEquipmentBase
from sample import Sample, Base as SampleBase

from sqlalchemy.orm import sessionmaker

class Database(object):

	def __init__(self):
		self.sqlite = 'sqlite:///tenergy.db'
		self.engine = create_engine(self.sqlite, echo=True)

	def drop(self):
		ChargeEquipment.__table__.drop(self.engine)
		Sample.__table__.drop(self.engine)

	def create(self):
		ChargeEquipmentBase.metadata.create_all(self.engine)
		SampleBase.metadata.create_all(self.engine)

	def createSession(self):
		Session = sessionmaker(bind=self.engine)
		self.db_session = Session()
		return self.db_session
	
	def find(self, clazz, where):
		session = self.createSession()
		query = session.query(clazz)
		query = query.filter(where)
		return query.all()

	def save(self, entity):
		session = self.createSession()
		session.add(entity)
		session.commit()

