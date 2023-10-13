CREATE_TABLE_CHECK = """
    CREATE TABLE IF NOT EXISTS Checks
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    tariff VARCHAR(255),
    user_id VARCHAR(255),
    user_name VARCHAR(255) NULL
    )
"""

INSERT_INTO_TABLE_CHECK = """
    INSERT INTO Checks(tariff, user_id, user_name) VALUES (?, ?, ?)
"""

CREATE_TABLE_PAYMENT_CHECK = """
    CREATE TABLE IF NOT EXISTS PaymentRequests
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    tariff VARCHAR(255),
    photo_check TEXT,
    user_id VARCHAR(255),
    user_name VARCHAR(255) NULL
    )
"""

INSERT_INTO_TABLE_PAYMENT_REQUEST = """
    INSERT INTO PaymentRequests(tariff, photo_check, user_id, user_name) VALUES (?, ?, ?, ?)
"""

SELECT_TARIFF_PROBNYI = """
    SELECT COUNT(*) FROM Checks WHERE user_id = ? AND tariff = 'Пробный'
"""