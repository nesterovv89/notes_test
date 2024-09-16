from sqlalchemy import Column, String, Text, DateTime, func
from datetime import datetime

from app.core.db import Base


class Note(Base):
    title = Column(String(50), unique=True, nullable=False)
    text = Column(Text)
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime, default=func.now(), onupdate=func.now())