import sqlite3

def run_sql_script():
    conn = sqlite3.connect("messagerie.db")
    cursor = conn.cursor()

    with open("scripts.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_sql_script()