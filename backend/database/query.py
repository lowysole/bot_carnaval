from backend.database.db_base import DBBase
from backend import settings


class Query(DBBase):

    def __init__(self, db_file):
        super(Query, self).__init__(db_file)

    def process_query(self, args):
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
