from env import datetime_now_tz

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChargeEquipment(Base, object):
    __tablename__ = 'ChargeEquipment'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Port = Column(String(40))
    Model = Column(String(40))
    Version = Column(String(40))
    VoltagePV = Column(Float)
    CurrentPV = Column(Float)
    PowerPV = Column(Float)
    PowerLowPV = Column(Float)
    PowerHighPV = Column(Float)
    VoltageBattery = Column(Float)
    CurrentBattery = Column(Float)
    PowerBattery = Column(Float)
    PowerLowBattery = Column(Float)
    PowerHighBattery = Column(Float)
    ChargingMode = Column(Integer)
    ChargingModeName = Column(String(30))
    CurrentOfLoad = Column(Float)
    CreatedDate = Column(DateTime(timezone=True), default=datetime_now_tz)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def to_json(self):
        return {
            'Id': self.Id,
            'Port': self.Port,
            'Model': self.Model,
            'Version': self.Version,
            'CurrentOfLoad': self.CurrentOfLoad,
            'ChargingMode': self.ChargingModeName,
            'CreatedDate': None if self.CreatedDate is None else self.CreatedDate.isoformat(),
            'pv': {
                'voltage': self.VoltagePV,
                'current': self.CurrentPV,
                'power': self.PowerPV,
            },
            'battery': {
                'voltage': self.VoltageBattery,
                'current': self.CurrentBattery,
                'power': self.PowerBattery,
            },
        }
