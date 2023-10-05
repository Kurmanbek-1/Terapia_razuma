CREATE_TABLE_CHECK = """
    CREATE TABLE IF NOT EXISTS Checks
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_check TEXT,
    user_id VARCHAR(255),
    user_name VARCHAR(255) NULL
    )
"""
