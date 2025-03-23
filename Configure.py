from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Updated connection string
# DATABASE_URI = r"mssql+pyodbc://sa:habibfarooq12345@DESKTOP-8TUN3M3\SQLEXPRESS\SQLEXPRESS/biitCourseAdvisorChatbot?driver=ODBC+Driver+17+for+SQL+Server"

DATABASE_URI = "mssql+pyodbc://sa:habibfarooq12345@DESKTOP-8TUN3M3\SQLEXPRESS/biitCourseAdvisorChatbot?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
