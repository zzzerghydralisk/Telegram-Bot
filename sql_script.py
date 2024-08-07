import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tg_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_text TEXT NOT NULL,
            tg_id INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.close()

def add_request(tg_text, tg_id, status):
    conn = sqlite3.connect('Telegram_DB.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tg_table (tg_text, tg_id, status)
        VALUES (?, ?, ?)
    """, (tg_text, tg_id, status))
    conn.commit()
    conn.close()

def read_all_rows(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM tg_table")
    rows = cursor.fetchall()
    conn.close()
    return rows

def adding_to_db(list):
    for x in list:
       add_request(x['text'], x['id'], x['status'])

def get_records(db_file,status,ids):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT  *  FROM tg_table WHERE status = ? ORDER BY id = ?", (status, ids))
    records = cursor.fetchall()

    conn.close()
    return (records)

def update_status(db_file, id, new_status):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE tg_table SET status = ? WHERE id = ?", (new_status, id))
    conn.commit()
    conn.close()

def update_text(db_file, id, tg_text):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("UPDATE tg_table SET tg_text = ? WHERE id = ?", (tg_text, id))
    conn.commit()
    conn.close()

