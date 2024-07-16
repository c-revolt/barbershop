from sqlalchemy import DateTime, String, Float, func, BigInteger, Numeric, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # Поля которые указывают дату создания базы данных и измнения
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    time: Mapped[str] = mapped_column(String(3), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(4), nullable=False)


class Barber(Base):
    __tablename__ = "barber"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    photo: Mapped[str] = mapped_column(String(150))
    earnings: Mapped[float] = mapped_column(Numeric, default=0.0)
    completed_jobs: Mapped[int] = mapped_column(Integer, default=0)






# class User(Base):
#     __tablename__ = "user"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
#     first_name: Mapped[str] = mapped_column(String(150), nullable=True)
#     applications: Mapped[str] = mapped_column() ????
#     phone: Mapped[str] = mapped_column(String(13), nullable=True)
#
#
# class SubScription(Base):
#     __tablename__ = "subscription"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(150), nullable=False)
#     description: Mapped[str] = mapped_column(String(150), nullable=False)
#     price: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
#
# class Application(Base):
#     __tablename__ = "application"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
