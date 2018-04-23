import os
import time
import jwt
import datetime
import hashlib

from env import log, config

from entity.database import Database

from entity.user import User

from sqlalchemy import func, desc

from flask_login import UserMixin

serve = config.get('serve')
secret_key = serve['secret_key']

logger = log(__name__)


class UserSession(UserMixin):
    def __init__(self, first_name, last_name, session_token):
        self.first_name = first_name
        self.last_name = last_name
        self.session_token = session_token

    def get_id(self):
        return unicode(self.session_token)

    def __repr__(self):
        return "%s" % (self.session_token)


class UserService(object):
    def __init__(self, database=None):
        if database is None:
            raise ValueError('database is NULL')

        self.database = database

    @staticmethod
    def create_user():
        user = User()
        user.FirstName = 'Admin'
        user.LastName = 'System'
        user.Username = 'admin'
        user.Password = hashlib.md5("admin").hexdigest()
        user.Email = 'admin@tenergy.com.br'
        return user

    def save_user(self, user):
        logger.info('save_user() user: {0}'.format(user))
        self.database.save(user)
        return user

    def login_user(self, username, password):
        logger.info('login_user() username: {0}'.format(username))

        password_new = hashlib.md5(password).hexdigest()

        session = self.database.create_session()
        query = session.query(User).filter(User.Username == username, User.Password == password_new)
        query = query.order_by(desc(User.CreatedDate))
        user = query.first()

        if user is None:
            return None

        auth_token = UserService.encode_auth_token(user)
        user_session = UserSession(user.FirstName, user.LastName, auth_token)
        return user_session

    @staticmethod
    def get_user_by_session(session_id):
        logger.info('get_user_by_session() session_id: {0}'.format(session_id))

        if session_id is None:
            return None

        payload = UserService.decode_auth_token(session_id)

        if payload is None:
            return None

        first_name = payload.get('FirstName')
        last_name = payload.get('LastName')

        return UserSession(first_name, last_name, session_id)

    @staticmethod
    def encode_auth_token(user):
        """
            Generates the Auth Token
            :return: string
        """

        try:
            second_exp = 60 * 10
            datetime_now = datetime.datetime.utcnow()
            datetime_exp = datetime_now + datetime.timedelta(days=0, seconds=second_exp)

            payload = {
                'exp': datetime_exp,
                'iat': datetime_now,

                'Username': user.Username,
                'FirstName': user.FirstName,
                'LastName': user.LastName
            }
            return jwt.encode(payload, secret_key, algorithm='HS256')

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, secret_key)
            return payload

        except jwt.ExpiredSignatureError:
            logger.error('jwt.ExpiredSignatureError: Signature expired.')
            return None

        except jwt.InvalidTokenError:
            logger.error('jwt.InvalidTokenError: Invalid token.')
            return None


if __name__ == "__main__":
    database = Database.get_instance()
    user_service = UserService(database)

    session = user_service.database.create_session()
    query = session.query(User.Id, User.Username)
    query = query.filter(User.Username == 'admin')
    query = query.order_by(desc(User.CreatedDate))

    userList = query.all()

    print userList

    if len(userList) == 0:
        userAdmin = UserService.create_user()
        user_service.save_user(userAdmin)
