import sqlite3

def init_database():
    # This automatically creates a 'company.db' file in your folder
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    
    # 1. Create a mock users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            role TEXT,
            email TEXT,
            salary INTEGER
        )
    """)
    
    # 2. Insert mock data (including sensitive salary and email info)
    mock_users = [
        (1, 'Alice Smith', 'Engineering Lead', 'alice@company.com', 140000),
        (2, 'Bob Jones', 'Product Manager', 'bob@company.com', 120000),
        (3, 'Charlie Brown', 'UX Designer', 'charlie@company.com', 95000)
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?)", mock_users)
    conn.commit()
    conn.close()
    print("Database 'company.db' initialized with mock corporate data!")

if __name__ == "__main__":
    init_database()