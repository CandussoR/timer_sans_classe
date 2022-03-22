import sqlite3
from re import split

CREATE_TASK_TABLE = '''
      CREATE TABLE IF NOT EXISTS tasks (
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      task_name TEXT NOT NULL,
      subtask TEXT,
      UNIQUE (task_name, subtask));
      '''

CREATE_TIMER_TABLE = '''
    CREATE TABLE IF NOT EXISTS timer_data(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    date REAL,
    time_beginning REAL,
    time_ending REAL,
    time_elapsed REAL,
    FOREIGN KEY (task_id)
        REFERENCES tasks (id)
        );
    '''

CHECK_TASK_EXISTENCE = 'SELECT id FROM tasks WHERE task_name=(?);'

INSERT_NEW_TASK = 'INSERT INTO tasks (task_name) VALUES (?);'

RETRIEVE_ID ='SELECT id FROM tasks WHERE task_name=(?);'

CHECK_TUPLE_EXISTENCE = 'SELECT id FROM tasks WHERE task_name=(?) AND subtask=(?);'

INSERT_NEW_TUPLE = 'INSERT INTO tasks (task_name, subtask) VALUES (?, ?);'

RETRIEVE_TUPLE_ID = 'SELECT id FROM tasks WHERE task_name=(?) AND subtask=(?);'

def connect():
    connexion = sqlite3.connect('timer_data.db')
    return connexion

def create_tables(connexion):
    with connexion:
        connexion.execute(CREATE_TIMER_TABLE)
        connexion.execute(CREATE_TASK_TABLE)

def parse_input(task_input):
    parsed = split('\W', task_input, 1)
    return parsed[0], parsed[1]

def check_existence(connexion, *task):
    with connexion:
        if len(task) == 2 :
            result = connexion.execute(CHECK_TUPLE_EXISTENCE, [*task]).fetchone()
        else :
            result = connexion.execute(CHECK_TASK_EXISTENCE, [*task]).fetchone()
    return result[0]

def insert_new_task(connexion, *task):
    with connexion:
        if len(task) == 2 :
            connexion.execute(INSERT_NEW_TUPLE, [*task])
        else:
            connexion.execute(INSERT_NEW_TASK, [*task])

def fetch_id(connexion, *task):
    with connexion:
        retrieved_id = []
        if len(task) == 2 :
            retrieved_id += connexion.execute(RETRIEVE_TUPLE_ID, [*task]).fetchone()
        else:
            retrieved_id += connexion.execute(RETRIEVE_ID, [*task]).fetchone()
    return retrieved_id[0]