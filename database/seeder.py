try:
    import sqlite3 as sql
except ImportError as eImp:
    print(f"The following import error ocurred in file {__file__}: {eImp}")

def create_connection(db_path):
    conn = sql.connect(db_path)
    cursor = conn.cursor()

    return conn, cursor

def create_db(db_path):
    conn, cursor = create_connection(db_path)

    cursor.execute("CREATE TABLE users (name text, last_name text, age integer, mail text)")
    conn.commit()
    conn.close()

def add_values(db_path):
    conn, cursor = create_connection(db_path)
    
    data = [
        ("Diego", "sepsi bebe", 10, "diego@gmail.com"),
        ("Vanessa", "crayola chida", 15, "vane@gmail.com"),
        ("Anai", "gutierrez espinosa", 20, "anai@gmail.com"),
        ("Eder", "sepsi bebe", 25, "eder@gmail.com"),
        ("Carolina", "neo cortex", 22, "caro@gmail.com"),
        ("Nenex", "ederxitop bebe", 21, "nenex@gmail.com")
    ]

    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    DB_PATH = "D:\\github projects\\sqlAlchemyPydantic\\database\\users.db"

    try:
        create_db(DB_PATH)
        add_values(DB_PATH)
    except Exception as ex:
        print(f"The following error ocurred: {ex}")