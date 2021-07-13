import sqlite3
DATABASE_NAME = "endpoints.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS endpoints(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT NOT NULL,
            hits INTEGER,
            isActive BOOLEAN DEFAULT True,
            createdTime TEXT
            )""", 
        """CREATE TABLE IF NOT EXISTS payloads(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint_id INTEGER,
            headers STRING,
            data STRING,
            queryParameter STRING,
            
            CONSTRAINT fk_endpoint_id
                FOREIGN KEY (endpoint_id)
                REFERENCES endpoints(id)
        )
        """
    ]
    
    db = get_db()
    cursor = db.cursor()
    
    for table in tables:
        cursor.execute(table)