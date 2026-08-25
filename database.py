import sqlite3
import os

DB_NAME = "database.db"

def init_db():
    """Initializes the database and creates the hierarchical renstra_iku table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create a structured table capable of handling multi-level organizational cascading
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS renstra_iku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            code TEXT NOT NULL,
            title TEXT NOT NULL,
            aspect TEXT,
            target TEXT,
            owner_post TEXT NOT NULL,
            parent_code TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_iku(level, code, title, aspect, target, owner_post, parent_code):
    """Inserts a structured strategic indicator into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO renstra_iku (level, code, title, aspect, target, owner_post, parent_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (level, code, title, aspect, target, owner_post, parent_code))
    
    conn.commit()
    conn.close()

def get_all_iku():
    """Retrieves all strategic indicators sorted by organizational level hierarchy."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, level, code, title, aspect, target, owner_post, parent_code FROM renstra_iku')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def clear_all_iku():
    """Wipes out the current data feed to allow a clean reload of Renstra metrics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM renstra_iku')
    conn.commit()
    conn.close()

def update_iku(record_id, level, code, title, aspect, target, owner_post, parent_code):
    """Updates an existing strategic indicator record in the database by its ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE renstra_iku
        SET level = ?, code = ?, title = ?, aspect = ?, target = ?, owner_post = ?, parent_code = ?
        WHERE id = ?
    ''', (level, code, title, aspect, target, owner_post, parent_code, record_id))
    
    conn.commit()
    conn.close()

# Enforce initialization upon loading the module
init_db()

def init_sotk_table():
    """Creates the master SOTK mandates table for organizational blueprint alignment."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Removed python-style comments inside the raw SQL execution block to avoid SQLite syntax errors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sotk_mandates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unit_level TEXT NOT NULL,
            post_name TEXT NOT NULL,
            parent_post TEXT,
            main_duty TEXT NOT NULL,
            functions TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def insert_sotk(unit_level, post_name, parent_post, main_duty, functions=None):
    """Inserts a structural post and its legal mandates into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sotk_mandates (unit_level, post_name, parent_post, main_duty, functions)
        VALUES (?, ?, ?, ?, ?)
    ''', (unit_level, post_name, parent_post, main_duty, functions))
    
    conn.commit()
    conn.close()

def get_sub_units_by_parent(parent_name):
    """Retrieves all immediate downline positions and their legal duties for the LLM context."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT post_name, main_duty, functions 
        FROM sotk_mandates 
        WHERE parent_post = ?
    ''', (parent_name,))
    
    rows = cursor.fetchall()
    conn.close()
    return rows

# Automatically expand the schema without wiping your existing data
init_sotk_table()

# Append this code at the very bottom of database.py

def init_mph_table():
    """Creates the matrix of role results (MPH) cell storage table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mph_cells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            division_name TEXT NOT NULL,
            superior_code TEXT NOT NULL,
            subordinate_post TEXT NOT NULL,
            cascaded_sasaran TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_or_update_mph_cell(division_name, superior_code, subordinate_post, cascaded_sasaran):
    """Saves or updates a single intersection cell within the MPH matrix."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM mph_cells 
        WHERE division_name = ? AND superior_code = ? AND subordinate_post = ?
    ''', (division_name, superior_code, subordinate_post))
    row = cursor.fetchone()
    
    if row:
        cursor.execute('''
            UPDATE mph_cells SET cascaded_sasaran = ? WHERE id = ?
        ''', (cascaded_sasaran, row[0]))
    else:
        cursor.execute('''
            INSERT INTO mph_cells (division_name, superior_code, subordinate_post, cascaded_sasaran)
            VALUES (?, ?, ?, ?)
        ''', (division_name, superior_code, subordinate_post, cascaded_sasaran))
        
    conn.commit()
    conn.close()

def get_mph_matrix_data(division_name):
    """Retrieves all saved matrix cell entries for a specific division to build a lookup dict."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT superior_code, subordinate_post, cascaded_sasaran FROM mph_cells
        WHERE division_name = ?
    ''', (division_name,))
    rows = cursor.fetchall()
    conn.close()
    
    # Transform to a dictionary lookup: {(superior_code, subordinate_post): cascaded_sasaran}
    matrix_dict = {}
    for superior_code, subordinate_post, cascaded_sasaran in rows:
        matrix_dict[(superior_code, subordinate_post)] = cascaded_sasaran
    return matrix_dict

# Initialize the new MPH table schema immediately upon module import
init_mph_table()