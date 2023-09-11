from sqlalchemy import (BLOB, BigInteger, Column, ForeignKey, Integer, Numeric,
                        String)
from sqlalchemy.orm import relationship

from database import Base


class Challenge(Base):
    __tablename__ = "CHALLENGE"
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(30), nullable=False)
    domain = Column(String(500), nullable=False)


class Youtube(Base):
    __tablename__ = "YOUTUBE"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    hits = Column(BigInteger, nullable=False)
    likes = Column(Integer, nullable=False, default=0)
    url = Column(String(500), nullable=False)
    challenge = Column(Integer, ForeignKey("CHALLENGE.id"), nullable=False)
    title = Column(String(500), nullable=False)
    channel = Column(String(100), nullable=False)
    thumbnail = Column(BLOB, nullable=True)
