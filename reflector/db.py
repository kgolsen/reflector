import pickle
from urllib.parse import quote

from sqlalchemy import *


class Reflector:

    def __init__(self, config):
        assert {'host', 'port', 'user', 'password', 'database', 'sql-driver'} <= config.keys()
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
        self.tables = {}
        self.views = {}
        self._init_sql()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['sql']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._init_sql()

    def _init_sql(self):
        self.sql = create_engine(self.connection_string)
        self.meta = inspect(self.sql)

    def persist(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def restore(cls, file):
        with open(file, 'rb') as f:
            obj = pickle.load(f)
            assert isinstance(obj, cls)
            return obj

    def reflect(self):
        for tbl in self.meta.get_table_names():
            self.tables[tbl] = {
                'columns': self.meta.get_columns(tbl),
                'primary_key': self.meta.get_pk_constraint(tbl),
                'foreign_keys': self.meta.get_foreign_keys(tbl),
            }
