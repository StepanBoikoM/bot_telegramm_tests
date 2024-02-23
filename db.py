#БАЗА ДАННЫХ
import  sqlite3

def check_table():
    # Путь к файлу базы данных SQLite // ЗАМЕНИТЬ НА СВОЙ
    db_path = "C:\\Users\\My PC\\Desktop\\bot_tg\\sql.db"

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS sql (
        ID INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        patronymic TEXT,
        work_number TEXT,
        phone_number TEXT,
        id_telegramm TEXT,
        status TEXT)''')

    conn.commit()
    cur.close()
    conn.close()


check_table()