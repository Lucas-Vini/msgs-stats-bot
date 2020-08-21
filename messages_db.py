import sqlite3

def save_message(msg, date, user, chat):
    chat = abs(chat)
    user = abs(user)
    if table_existence(chat) == False:
        create_table(chat)
    insert_message(user, msg, date, chat)

def create_table(name):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    create_table = """
        CREATE TABLE table_name (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        message TEXT NOT NULL,
        date DATE NOT NULL
    );
    """
    create_table = create_table.replace("table_name", "t"+str(name))
    cursor.execute(create_table)        
    conn.close()

def table_existence(name):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
        """)
    for table in cursor.fetchall():
        if table[0] == ('t' + str(name)):
            conn.close()
            return True
    conn.close()
    return False

def insert_message(user, msg, date, chat):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    insert_values = """
    INSERT INTO table_name (name, message, date)
    VALUES ('name_value', 'message_value', 'date_value')
    """
    insert_values = insert_values.replace('table_name', 't'+str(chat))
    insert_values = insert_values.replace('name_value', str(user))
    insert_values = insert_values.replace('message_value', msg)
    insert_values = insert_values.replace('date_value', date)
    cursor.execute(insert_values)
    conn.commit()
    conn.close()

def get_all_messages(chat):
    chat = abs(chat)
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    select_messages = """
    SELECT message FROM table_name;
    """
    select_messages = select_messages.replace('table_name','t'+str(chat))
    cursor.execute(select_messages)
    all_messages = " ".join(msg[0] for msg in cursor.fetchall())
    return all_messages

def get_user_messages(user, chat):
    chat = abs(chat)
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    select_messages = """
    SELECT message FROM table_name WHERE name = user_id;
    """
    select_messages = select_messages.replace('table_name','t'+str(chat))
    select_messages = select_messages.replace('user_id',str(user))
    cursor.execute(select_messages)
    user_messages = " ".join(msg[0] for msg in cursor.fetchall())
    return user_messages

def count_users_messages(chat):
    chat = abs(chat)
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    select_users = """
    SELECT name FROM table_name;
    """
    select_users = select_users.replace('table_name','t'+str(chat))
    cursor.execute(select_users)
    users_count = {}
    for user in cursor.fetchall():
        if user[0] in users_count:
            users_count[user[0]] += 1
        else:
            users_count[user[0]] = 1
    return users_count
