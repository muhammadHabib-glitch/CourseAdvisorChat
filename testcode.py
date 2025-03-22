import pyodbc

connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-8TUN3M3\\SQLEXPRESS;DATABASE=CourseAdvisorChatbot;UID=sa;PWD=habibfarooq12345"

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
