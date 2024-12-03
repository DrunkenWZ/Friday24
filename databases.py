import sqlite3


def create_database():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()


def save_task_to_history(user_id, type_of_task, input_text):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO history (user_id, task_type, text_task)
        VALUES (?, ?, ?)
    ''', (user_id, type_of_task, input_text))
    
    conn.commit()
    conn.close()