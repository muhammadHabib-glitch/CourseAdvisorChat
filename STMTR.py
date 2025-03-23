from sqlalchemy import String, Column

from Model.Configure import Base

class STMTR(Base):
    __tablename__ = 'STMTR'
    Reg_No=Column(String(14),primary_key=True,nullable=False)
    St_firstname=Column(String(25),nullable=True)
    St_lastname = Column(String(25), nullable=True)
    Password=Column(String(50),nullable=True)