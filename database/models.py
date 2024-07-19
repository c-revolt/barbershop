from sqlalchemy import DateTime, String, Float, func, BigInteger, Numeric, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
    description: Mapped[str] = mapped_column(String(100))
    photo: Mapped[str] = mapped_column(String(150))
    earnings: Mapped[float] = mapped_column(Numeric, default=0.0)
    completed_jobs: Mapped[int] = mapped_column(Integer, default=0)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(30), nullable=True)
    user_phone: Mapped[str] = mapped_column(String(12), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    # bookings: Mapped[list["Booking"]] = relationship("Service", back_populates="user")


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sum_order: Mapped[float] = mapped_column(Numeric)
    order_service: Mapped[str] = mapped_column(Text)
    user_telegram_id: Mapped[str] = mapped_column(BigInteger)
    order_status: Mapped[int] = mapped_column(Integer)




# class Booking(Base):
#     __tablename__ = 'booking'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey('clients.id'), nullable=False)
#     service: Mapped[str] = mapped_column(String, nullable=False)
#     date: Mapped[str] = mapped_column(String, nullable=False)
#     time: Mapped[str] = mapped_column(String, nullable=False)
#
#     user: Mapped["User"] = relationship("User", back_populates="booking")
#     barber: Mapped["Barber"] = relationship("Barber", back_populates="barber")
