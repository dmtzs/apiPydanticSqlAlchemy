try:
    from app import database
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

class Users(database.Model):
    rowid = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    last_name = database.Column(database.String(150), nullable=False)
    age = database.Column(database.Integer, nullable=False)
    mail = database.Column(database.String(150), unique=True, nullable=False)

    def __init__(self, name, last_name, age, mail):
        super().__init__()
        self.name = name
        self.last_name = last_name
        self.age = age
        self.mail = mail

    def serializer(self):
        return {
            "rowid": self.rowid,
            "name": self.name,
            "last_name": self.last_name,
            "age": self.age,
            "mail": self.mail
        }