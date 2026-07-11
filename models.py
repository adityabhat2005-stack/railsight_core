from sqlalchemy import Column, Integer, String, Numeric, Time, ForeignKey
from database import Base

class TrainCategory(Base):
    __tablename__ = "train_category"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)
    base_fare_per_km = Column(Numeric(5, 2), nullable=False)

class TrainMaster(Base):
    __tablename__ = "train_master"
    train_no = Column(String(20), primary_key=True)
    train_name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("train_category.category_id", ondelete="CASCADE"))

class LiveSchedules(Base):
    __tablename__ = "live_schedules"
    schedule_id = Column(Integer, primary_key=True)
    train_no = Column(String(20), ForeignKey("train_master.train_no", ondelete="CASCADE"))
    source_station = Column(String(10), default="MJS")
    dest_station = Column(String(10), default="MAQ")
    distance_km = Column(Numeric(5, 2), nullable=False)
    scheduled_departure = Column(Time, nullable=False)
    delay_minutes = Column(Integer, default=0)
