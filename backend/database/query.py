from backend.database.db_base import DBBase
from backend.database import importer
from backend import settings

DAY_TMP = """CREATE TABLE IF NOT EXISTS day_tmp(
        chat_id int,
        day text
        );"""

class Query(DBBase):

    def __init__(self, db_file):
        super(Query, self).__init__(db_file)
        self._create_tables()

    def process_query(self, args):
        try:
            day = args[0].lower().split( )[0]
            hour = float(args[1])
            data = self._extract_info(day, hour)
            data_list = [list(i) for i in data]
            for row in data_list:
                row[1] = self._get_day_num(row[1])
                hour = str(row[2]).replace('.', ':', 1)
                if len(hour) == 5:
                    row[2] = hour + ' h'
                else:
                    row[2] = hour + '0 h'
            return data_list
        except:
            return []

    def add_tmp_day(self, chat_id, day):
        self._add_tmp_day(chat_id, day)
        self.conn.commit()

    def get_tmp_day(self, chat_id):
        day = self._get_tmp_day(chat_id)
        self._remove_tmp_day(chat_id)
        self.conn.commit()
        return day

    def _extract_info(self, day, hour):
        query = """
            SELECT
                title,
                day,
                hour,
                place,
                description
                FROM program
                WHERE day = ?
                AND hour >= ?
                ORDER BY hour asc limit 3;
            """
        data = [day, hour]
        return self._get_sql(query, data=data, iterate=True)

    def _get_day_num(self, day):
        if day == 'dijous':
            return 'Dijous 20'
        elif day == 'divendres':
            return 'Divendres 21'
        elif day == 'dissabte':
            return 'Dissabte 22'
        elif day == 'diumenge':
            return 'Diumenge 23'

    def _add_tmp_day(self, chat_id, day):
        query = """
            INSERT INTO day_tmp
            (chat_id, day)
            VALUES (?,?)
            """
        data = [chat_id, day]
        cur = self.conn.cursor()
        cur.execute(query, data)

    def _get_tmp_day(self, chat_id):
        query = """
            SELECT day from day_tmp
            WHERE chat_id = ?
            """
        cur = self.conn.cursor()
        return self._get_sql(query, data=[chat_id])

    def _remove_tmp_day(self, chat_id):
        query = """
            DELETE FROM day_tmp
            WHERE chat_id = ?
            """
        cur = self.conn.cursor()
        cur.execute(query, [chat_id])

    def _create_tables(self):
        self._execute_sql(DAY_TMP)
        self.conn.commit()
