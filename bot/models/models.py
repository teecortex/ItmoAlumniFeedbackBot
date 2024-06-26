from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, INT, BIGINT, Boolean, ForeignKey, Date
import datetime

Base = declarative_base()

class Menti(Base):
    __tablename__ = "menti"

    id = Column(type_=INT, primary_key=True, autoincrement=True)
    isu = Column(type_=INT, name="isu", unique=True, nullable=False)
    name = Column(type_=String)
    surname = Column(type_=String)
    patronymic = Column(type_=String)
    telegram_id = Column(type_=BIGINT, nullable=False, name="telegram_id", unique=True)
    email = Column(type_=String, nullable=False, name="email", unique=True)

    feedbacks = relationship("Feedback")


class Mentor(Base):
    __tablename__ = "mentor"

    id = Column(type_=INT, primary_key=True, autoincrement=True)
    name = Column(type_=String)
    surname = Column(type_=String)
    telegram_id = Column(type_=BIGINT, nullable=False, name="telegram_id", unique=True)
    is_active = Column(type_=Boolean, default=True)

    feedback = relationship("Feedback")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(type_=INT, primary_key=True, autoincrement=True, name="id")
    menti_id = Column(INT, ForeignKey("menti.id"), nullable=False)
    mentor_id = Column(INT, ForeignKey("mentor.id"), nullable=False)
    mentis_rate = Column(type_=INT)
    instruments = Column(type_=String)
    interaction_problems = Column(type_=String)
    org_problems = Column(type_=String)
    suggestions = Column(type_=String)
    date_of_feedback = Column(type_=Date, nullable=False, default=datetime.datetime.now())




