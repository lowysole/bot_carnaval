#!/usr/bin/env python
import argparse

from backend.database import importer
from backend import settings

if __name__ == '__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument('input_file',
                        help='Format: id,title,day,hour,place,description')
    args = parser.parse_args()
    input_file = args.input_file

    imp = importer.Importer(settings.DB_FILE)
    imp.import_program(input_file)
    imp.close()
