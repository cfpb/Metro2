# defines the evaluator class and list of evaluators
import logging

from iterator_file import IteratorFile
from tables import connect


class Evaluator():
    date_format = "MMDDYYYY"
    strptime_format = "%m%d%Y"

    def __init__(self, name, fields, func=None, longitudinal_func=None):
        self.name = name
        self.fields = fields
        self.func = func
        self.longitudinal_func = longitudinal_func

    def exec_custom_func(self, connection=None, engine=None):
        # returns a list of results from running a query
        res = list()
        if self.longitudinal_func:
            res = self.longitudinal_func(connection, engine)
        else:
            res = connection.execute(self.func())

        # returns a list of dicts from the results
        res_set = [dict(zip(row.keys(), row)) for row in res]

        return res_set

# copy to previously created temp table
def copy_to_temp(res_set):
    logger = logging.getLogger('evaluator.copy_to_temp')
    conn = None
    # create a new connection and cursor using just psycopg2 (not SQLAlchemy)
    # use copy from function to copy results to temp_tbl
    try:
        conn = connect()
        cur = conn.cursor()

        block_start = 0
        block_size = 2000
        tup_set = tuple(res_set)
        sub = list()
        sub.append('{}')
        # the length of each result will be the same.
        commands = '\t'.join(sub * (len(tup_set[block_start])))

        while (block_start + block_size) < len(tup_set):
            block_end = block_start + block_size
            # split values
            val_list = tup_set[block_start:block_end]

            copy = IteratorFile((commands.format(*vals) for vals in val_list))

            cur.copy_from(copy, 'temp_tbl')
            # persist changes
            conn.commit()

            block_start += block_size

        # if start is still less than the length of results, do one more copy
        if block_start < len(tup_set):
            # split values
            val_list = tup_set[block_start:len(tup_set)]

            copy = IteratorFile((commands.format(*vals) for vals in val_list))

            cur.copy_from(copy, 'temp_tbl')

        cur.close()
        # persist changes
        conn.commit()

    except Exception as e:
        logger.error(f"An exception occurred while trying to create a cursor: {e}")
    finally:
        if conn is not None:
            conn.close()
