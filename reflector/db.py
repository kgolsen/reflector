import pickle
from urllib.parse import quote

from sqlalchemy import *


class Inspector:

    def __init__(self, config):
        assert {'host', 'port', 'user', 'password', 'database', 'sql-driver'} < config.keys()
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = quote(config['password'], safe='')
        self.database = config['database']
        self.sql_driver = config['sql-driver']
        self.connection_string = f"{self.sql_driver}://" \
                                 f"{self.user}:{self.password}" \
                                 f"@{self.host}:{self.port}/" \
                                 f"{self.database}"

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['sql']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._init_sql()

    def _init_sql(self):
        self.sql = create_engine(self.connection_string)

    def persist(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def restore(cls, file):
        with open(file, 'rb') as f:
            obj = pickle.load(f)
            assert isinstance(obj, cls)
