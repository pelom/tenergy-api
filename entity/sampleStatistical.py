from env import datetime_now_tz

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

from chargeEquipment import ChargeEquipment

Base = declarative_base()


class SampleStatistical(Base):
    __tablename__ = 'SampleStatistical'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChargeEquipmentId = Column(Integer, ForeignKey(ChargeEquipment.Id), nullable=False)

    VoltageMaxPV = Column(Float)
    VoltageMinPV = Column(Float)

    VoltageMaxBattery = Column(Float)
    VoltageMinBattery = Column(Float)

    ConsumedEnergy = Column(Float)
    ConsumedEnergyLow = Column(Float)
    ConsumedEnergyHigh = Column(Float)

    GeneratedEnergy = Column(Float)
    GeneratedEnergyLow = Column(Float)
    GeneratedEnergyHigh = Column(Float)

    BatteryCurrent = Column(Float)
    BatteryCurrentLow = Column(Float)
    BatteryCurrentHigh = Column(Float)
    BatteryTemp = Column(Float)

    AmbientTemp = Column(Float)
    CreatedDate = Column(DateTime(timezone=True), default=datetime_now_tz())

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def to_json(self):
        return {
            'Id': self.Id,
            'VoltageMaxPV': self.VoltageMaxPV,
            'VoltageMinPV': self.VoltageMinPV,
            'VoltageMaxBattery': self.VoltageMaxBattery,
            'VoltageMinBattery': self.VoltageMinBattery,
            'ConsumedEnergy': self.ConsumedEnergy,
            'ConsumedEnergyLow': self.ConsumedEnergyLow,
            'ConsumedEnergyHigh': self.ConsumedEnergyHigh,
            'GeneratedEnergy': self.GeneratedEnergy,
            'GeneratedEnergyLow': self.GeneratedEnergyLow,
            'GeneratedEnergyHigh': self.GeneratedEnergyHigh,
            'BatteryCurrent': self.BatteryCurrent,
            'BatteryCurrentLow': self.BatteryCurrentLow,
            'BatteryCurrentHigh': self.BatteryCurrentHigh,
            'BatteryTemp': self.BatteryTemp,
            'AmbientTemp': self.AmbientTemp,
            'CreatedDate': None if self.CreatedDate is None else self.CreatedDate.isoformat(),
        }
