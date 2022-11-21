try:
    from app import database
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.String(100), nullable=False)
    last_name = database.Column(database.String(80), nullable=False)
    age = database.Column(database.Integer, nullable=False)

    def __init__(self, id, username, password, last_name, age) -> None:
        super().__init__()
        self.id = id
        self.username = username
        self.password = password
        self.last_name = last_name
        self.age = age
    
    def serializer(self) -> dict:
        obj_serialized = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "last_name": self.last_name,
            "age": self.age
        }
        return obj_serialized