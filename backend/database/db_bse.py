import logging
import sqlite3

logger = logging.getLogger(__name__)


INDEX = "CREATE INDEX IF NOT EXISTS {} ON {} ({})"

class DBBase:

    def __init__(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.text_factory = str
        except Exception as e:
            logger.error(e)
            raise

    def _execute_sql(self, query):
        """Execute query
        :param query: a query statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(query)
        except Exception as e:
            logger.error(e)
            raise

    def _create_index(self, table_name, column_name):
        index_name = "{}__{}".format(table_name, column_name)
        self._execute_sql(INDEX.format(index_name, table_name, column_name))
        self.conn.commit()

    def _get_sql(self, query, data=[], iterate=False):
        """ Fetch a query, use iterate to obtain the cursor
        :param query: a query statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(query, data)
            if iterate:
                return c
            return c.fetchall()
        except Exception as e:
            logger.error(e)
            raise

    def close(self):
        self.conn.close()
