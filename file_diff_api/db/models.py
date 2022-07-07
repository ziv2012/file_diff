from db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbTransaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    comp_id = Column(Integer, ForeignKey('comparisons.id'))
    trans_id = Column(String)
    diff_type = Column(String)
    value_left = Column(String)
    value_right = Column(String)
    comparison = relationship('DbComparison', back_populates='transactions')


class DbComparison(Base):
    __tablename__ = 'comparisons'
    id = Column(Integer, primary_key=True, index=True)
    left_name = Column(String)
    right_name = Column(String)
    comp_date = Column(DateTime)
    transactions = relationship('DbTransaction', back_populates='comparison')
