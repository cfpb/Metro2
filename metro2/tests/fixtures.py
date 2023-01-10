# fixtures for testing

class Cursor():
    def execute(self, *_):
        return None

    def fetchall(self):
        return [("test", "success")]

    def close(self):
        return None

class Connect():
    def cursor(self):
        return Cursor()

    def close(self):
        return None
