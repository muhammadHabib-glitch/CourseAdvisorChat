from sqlalchemy import String, Integer,Column


from Model.Configure import Base

class KnowledgeBaseValue(Base):
    __tablename__ = 'KnowledgeBase'

    Key_Name = Column(String(50), primary_key=True, nullable=False)
    Type = Column(Integer, nullable=False)
    Value = Column(String(300), nullable=False)
    Status = Column(Integer, default=0)
