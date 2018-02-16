import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

from chargeEquipment import ChargeEquipment

Base = declarative_base()


class Sample(Base):
    __tablename__ = 'Sample'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChargeEquipmentId = Column(Integer, ForeignKey(ChargeEquipment.Id), nullable=False)

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

    VoltageDischarging = Column(Float)
    CurrentDischarging = Column(Float)
    PowerDischarging = Column(Float)
    PowerLowDischarging = Column(Float)
    PowerHighDischarging = Column(Float)

    BatterySOC = Column(Float)
    VoltageSystemBattery = Column(Float)
    TemperatureBattery = Column(Float)
    TemperatureRemoteBattery = Column(Float)
    TemperatureInsideEquipment = Column(Float)
    TemperaturePowerComponents = Column(Float)

    CodeStatusBattery = Column(Integer)
    StatusBattery = Column(String(40))

    CodeStatusEquipment = Column(Integer)

    CodeStatusDischarging = Column(Integer)
    StatusDischarging = Column(String(40))

    CodeStatusCharge = Column(Integer)
    StatusCharge = Column(String(40))

    CreatedDate = Column(DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def to_json(self):
        return {
            'Id': self.Id,
            'BatterySOC': self.BatterySOC,
            'VoltageSystemBattery': self.VoltageSystemBattery,
            'StatusBattery': self.StatusBattery,
            'StatusDischarging': self.StatusDischarging,
            'StatusCharge': self.StatusCharge,
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
            'discharging': {
                'voltage': self.VoltageDischarging,
                'current': self.CurrentDischarging,
                'power': self.PowerDischarging,
            },
            'temperature': {
                'Battery': self.TemperatureBattery,
                'RemoteBattery': self.TemperatureRemoteBattery,
                'InsideEquipment': self.TemperatureInsideEquipment,
                'PowerComponents': self.TemperaturePowerComponents,
            },
        }
