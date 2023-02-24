# fixtures for testing

class Cursor():
    def execute(self, *_):
        return [("expected", "sample", "data")]

    def fetchall(self):
        return [("test", "success")]

    def close(self):
        return None

class Connect():
    def cursor(self):
        return Cursor()

    def execute(self, *_):
        return [('a', 'b', 'c', 'd')]

    def close(self):
        return None

class Evaluator():
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func
        self.exam_number = 9999
        self.industry_type = ''

    def set_globals(self, ind_type, exam_num):
        self.exam_number = exam_num
        self.industry_type = ind_type

    def exec_custom_func(self):
        return self.func

eval1A = Evaluator("1A", "success", "success")
evaluators_test = [eval1A]
