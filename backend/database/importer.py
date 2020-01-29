from csv import DictReader
from backend.database.db_base import DBBase

PROGRAM = """CREATE TABLE IF NOT EXISTS program (
        id text,
        title text,
        day text,
        hour float,
        place text,
        description text
        );"""

class Importer(DBBase):

    def __init__(self, db_file):
        super(Importer, self).__init__(db_file)
        self._create_tables()

    def import_program(self, p_file):
        with open(p_file, 'rt') as fin:
            reader = DictReader(fin)
            for row in reader:
                self._create_program(row)
            self.conn.commit()

    def _create_program(self, row):

        row_table = (
            row.get('id'),
            row.get('title'),
            row.get('day'),
            row.get('hour'),
            row.get('place'),
            row.get('description')
        )
        sql = """ INSERT INTO program (
                id,
                title,
                day,
                hour,
                place,
                description)
                VALUES (?,?,?,?,?,?);
                """.replace("\n", "")
        cur = self.conn.cursor()
        cur.execute(sql, row_table)

    def _create_tables(self):
        self._execute_sql(PROGRAM)
        self._create_index("program", "id")
        self.conn.commit()
