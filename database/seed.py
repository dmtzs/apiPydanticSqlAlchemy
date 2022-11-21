try:
    import os
    import sqlite3 as sql
    from typing import Optional
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

def create_connection(db_path: str) -> Optional[tuple[sql.Connection, sql.Cursor]]:
    try:
        conn = sql.connect(db_path)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as c_conn:
        print(f"The following connection ERROR occurred in {__file__}: {c_conn}")
        return None

def create_db(db_path: str) -> None:
    conn, cursor = create_connection(db_path)

    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, last_name TEXT, age INTEGER)")
    conn.commit()
    conn.close()

def add_values(db_path: str) -> None:
    conn, cursor = create_connection(db_path)

    data = [
        (1, "user1", "pass1", "last 1", 20),
        (2, "user2", "pass2", "last 2", 21),
        (3, "user3", "pass3", "last 3", 22),
        (4, "user4", "pass4", "last 4", 23),
        (5, "user5", "pass5", "last 5", 24),
        (6, "user6", "pass6", "last 6", 25),
        (7, "user7", "pass7", "last 7", 26),
        (8, "user8", "pass8", "last 8", 27),
        (9, "user9", "pass9", "last 9", 28),
        (10, "user10", "pass10", "last 10", 29)
    ]

    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

    try:
        create_db(DB_PATH)
        add_values(DB_PATH)
    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")