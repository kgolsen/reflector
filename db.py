import pickle
from urllib.parse import quote

from sqlalchemy import create_engine, inspect, Table, MetaData


class Reflector:

    def __init__(self, *, sql_driver, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = quote(password, safe='')
        self.database = database
        self.sql_driver = sql_driver
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
