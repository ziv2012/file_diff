from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.orm import relationship


class DbRecord(Base):
    __tablename__ = 'records'
    rec_id = Column(Integer, primary_key=True, index=True)
    comp_id = Column(Integer)
    diff_type = Column(String)
    property_type = Column(String)
    value_left = Column(String)
    value_right = Column(String)


class DbComparison(Base):
    __tablename__ = 'comparisons'
    id = Column(Integer, primary_key=True, index=True)
    left_name = Column(String)
    right_name = Column(String)
    comp_date = Column(DateTime)
    rec_id = Column(Integer, ForeignKey('records.rec_id'))
