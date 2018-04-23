from sqlalchemy import create_engine

from user import User, Base as UserBase
from chargeEquipment import ChargeEquipment, Base as ChargeEquipmentBase
from sample import Sample, Base as SampleBase
from sampleStatistical import SampleStatistical, Base as SampleStatisticalBase

from sqlalchemy.orm import sessionmaker

from env import log, config

logger = log(__name__)


class Database(object):
    database_instance = None

    def __init__(self, config_base):
        echo = config_base.get('echo')
        self.sqlite = Database.build_url_database(config_base)
        self.engine = create_engine(self.sqlite, echo=echo)
        self.db_session = None
        create_drop = config_base.get('create_drop')
        if create_drop:
            self.drop()
            self.create()

    @staticmethod
    def build_url_database(config_base):
        logger.info('build_url_database()')

        host = config_base.get('host')
        db = config_base.get('db')
        url_database = '{0}{1}'.format(host, db)

        logger.debug('url_database: ' + url_database)

        return url_database

    def drop(self):
        logger.info('drop()')

        ChargeEquipment.__table__.drop(self.engine)
        Sample.__table__.drop(self.engine)
        SampleStatistical.__table__.drop(self.engine)

    def create(self):
        logger.info('create()')

        ChargeEquipmentBase.metadata.create_all(self.engine)
        SampleBase.metadata.create_all(self.engine)
        SampleStatisticalBase.metadata.create_all(self.engine)
        UserBase.metadata.create_all(self.engine)

    def create_session(self):
        logger.info('create_session()')

        session = sessionmaker(bind=self.engine)
        self.db_session = session()
        return self.db_session

    def find(self, clazz, where=None):
        logger.info('find() clazz: {0}, where: {1}'.format(clazz, where))

        session = self.create_session()
        query = session.query(clazz)
        if where is not None:
            query = query.filter(where)
        return query.all()

    def save(self, entity):
        logger.info('save() entity: {0}'.format(entity.__class__))

        session = self.create_session()
        session.add(entity)
        session.commit()

    @staticmethod
    def get_instance():
        logger.info('get_instance() database_instance: {0}'.format(Database.database_instance))

        if Database.database_instance is None:
            config_base = config.get('database')
            Database.database_instance = Database(config_base)
            Database.database_instance.create()
        return Database.database_instance
