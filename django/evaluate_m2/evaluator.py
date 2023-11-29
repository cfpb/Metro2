import logging

class Evaluator():
    date_format = "MMDDYYYY"
    strptime_format = "%m%d%Y"
    name: str

    def __init__(self, name, func=None, longitudinal_func=None):
        self.name = name
    # Do we need fields?
    #   self.fields = fields
        self.func = func
        self.longitudinal_func = longitudinal_func

    def exec_custom_func(self):
        # returns a list of results from running a query
        logger = logging.getLogger('evaluator.exec_custom_func')
        res = list()
        if self.longitudinal_func:
            res = self.longitudinal_func
        else:
            res = self.func
        print(res)
        # returns a list of dicts from the results
        res_set = [dict(zip(row._mapping.keys(), row)) for row in res]
        print(res_set)
        return res_set
