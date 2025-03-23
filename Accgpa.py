from sqlalchemy import String, Integer, Column, Float, DECIMAL, ForeignKey
from Model.Configure import Base

class Accgpa(Base):
    __tablename__ = 'Accgpa'

    REG_NO = Column(String(14), primary_key=True, nullable=False)
    SEMESTER_NO = Column(String(12), ForeignKey("SEMMTR.SEMESTER_NO"), primary_key=True, nullable=False)
    Q_PREV = Column(DECIMAL(5, 2), nullable=True)
    Q_CURR_SEM = Column(DECIMAL(5, 2), nullable=True)
    Q_TOTAL = Column(DECIMAL(6, 2), nullable=True)
    CR_PREV = Column(DECIMAL(6, 2), nullable=True)
    CR_CURR_SEM = Column(DECIMAL(6, 2), nullable=True)
    CR_TOTAL = Column(DECIMAL(6, 2), nullable=True)
    CGPA = Column(DECIMAL(6, 2), nullable=True)
    SECTION = Column(String(1), primary_key=True, nullable=False)
    SEM_STATUS = Column(String(10), nullable=True)
    Semc = Column(Integer, nullable=True)
    dropCount = Column(Integer, nullable=True)
