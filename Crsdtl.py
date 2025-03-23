


from sqlalchemy import String, Integer, Column, DateTime, Float, ForeignKey, DECIMAL

from Model.Configure import Base

class Crsdtl(Base):
    __tablename__ = 'Crsdtl'

    Course_no = Column(String(10), primary_key=True, nullable=False)
    ATTEMPT_NO = Column(String(10), nullable=False)
    REG_NO=Column(String(14),primary_key=True,nullable=False )
    SEMESTER_NO = Column(String(10), primary_key=True, nullable=False)
    SECTION = Column(String(10), nullable=False)
    Final_score = Column(DECIMAL(precision=5, scale=2), nullable=True)
    Midterm_score = Column(DECIMAL(precision=5, scale=2), nullable=True)
    Assi_score = Column(DECIMAL(precision=5, scale=2), nullable=True)
    Prac_score = Column(DECIMAL(precision=5, scale=2), nullable=True)
    Q_points = Column(DECIMAL(precision=5, scale=2), nullable=True)
    Grade = Column(String(10), nullable=True)
    DISCIPLINE = Column(String(20), nullable=False)
    SOS = Column(String(10), nullable=False)
    CrsSemNo = Column(Integer, nullable=True)


