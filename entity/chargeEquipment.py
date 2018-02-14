import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ChargeEquipment(Base):
	__tablename__ = 'ChargeEquipment'
	Id = Column(Integer, primary_key=True, autoincrement=True)
	Model            = Column(String(40))
	Version          = Column(String(40))
	VoltagePV        = Column(Float)
	CurrentPV        = Column(Float)
	PowerPV          = Column(Float)
	PowerLowPV       = Column(Float)
	PowerHighPV      = Column(Float)
	VoltageBattery   = Column(Float)
	CurrentBattery   = Column(Float)
	PowerBattery     = Column(Float)
	PowerLowBattery  = Column(Float)
	PowerHighBattery = Column(Float)
	ChargingMode     = Column(Integer)
	ChargingModeName = Column(String(30))
	CurrentOfLoad    = Column(Float)
	CreatedDate      = Column(DateTime, default=datetime.datetime.utcnow)
	
	def __str__(self):
		return str(self.__class__) + ": " + str(self.__dict__)

