import pickle
from urllib.parse import quote

from sqlalchemy import create_engine, inspect, Table, MetaData

PRIME_ONLY = 0
DEPENDENT_ONLY = 1
ALL_TABLES = 2


class Reflector:

    def __init__(self, *, sql_driver, host, port, user, password, database):
        self._host = host
        self._port = port
        self._user = user
        self._password = quote(password, safe='')
        self._database = database
        self._sql_driver = sql_driver
        self._connection_string = f"{self._sql_driver}://" \
                                 f"{self._user}:{self._password}" \
                                 f"@{self._host}:{self._port}/" \
                                 f"{self._database}"
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
        self.sql = create_engine(self._connection_string)
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
        m = MetaData()
        for tbl in self.meta.get_table_names():
            self.tables[tbl] = {
                'columns': self.meta.get_columns(tbl),
                'primary_key': self.meta.get_pk_constraint(tbl),
                'foreign_keys': self.meta.get_foreign_keys(tbl),
            }
        for view in self.meta.get_view_names():
            v = Table(view, m, autoload=True, autoload_with=self.sql)
            self.views[view] = {
                'columns': [{'name': c.name, 'type': c.type} for c in v.columns]
            }

    def get_tables(self, table_filter=ALL_TABLES):
        for tbl_name, tbl in self.tables.items():
            if table_filter == PRIME_ONLY:
                if 0 != len(tbl['foreign_keys']):
                    continue
            if table_filter == DEPENDENT_ONLY:
                if 0 == len(tbl['foreign_keys']):
                    continue
            yield tbl_name, tbl

    def get_views(self):
        for view_name, view in self.views.items():
            yield view_name, view

