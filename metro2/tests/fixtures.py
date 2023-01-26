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

    def close(self):
        return None

class Engine():
    def connect(self):
        return Connect()

    def dispose(self):
        return None

class Evaluator():
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func

    def set_globals(self, ind_type, exam_num):
        exam_number = exam_num
        industry_type = ind_type

    def exec_custom_func(self):
        return self.func()

evaluators = Evaluator("1A", "success", None)
