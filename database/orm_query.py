from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Service, Barber, User, Order


########### SERVICE ###########

async def orm_add_service(session: AsyncSession, data: dict):
    obj = Service(
        name=data.get("name", ""),
        time=data.get("time", ""),
        price=float(data.get("price", ""))
    )
    session.add(obj)
    await session.commit()

    # name = data.get("name", ""),
    # photo = data.get("photo", ""),
    # description = data.get("description", ""),
    # earnings = data.get("earnings", 0.0),
    # completed_jobs = data.get("completed_jobs", 0)


async def orm_get_services(session: AsyncSession):
    query = select(Service)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_service(session: AsyncSession, service_id: int):
    query = select(Service).where(Service.id == service_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_service(session: AsyncSession, service_id: int, data):
    query = update(Service).where(Service.id == service_id).values(
        name=data.get("name", ""),
        time=data.get("time", ""),
        price=float(data.get("price", "")),
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_service(session: AsyncSession, service_id: int):
    query = delete(Service).where(Service.id == service_id)
    await session.execute(query)
    await session.commit()


########### BARBER ###########
async def orm_add_barber(session: AsyncSession, data: dict):
    barber = Barber(
        name=data.get("name", ""),
        photo=data.get("photo", ""),
        description=data.get("description", ""),
        earnings=float(data.get("earnings", 0.0)),
        completed_jobs=data.get("completed_jobs", 0))

    session.add(barber)
    await session.commit()


async def orm_get_barbers(session: AsyncSession):
    query = select(Barber)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_update_barber(session: AsyncSession, barber_id: int, data):
    query = update(Barber).where(Barber.id == barber_id).values(
        name=data.get("name", ""),
        photo=data.get("photo", ""),
        description=data.get("description", ""),
        earnings=float(data.get("earnings", 0.0)),
        completed_jobs=data.get("completed_jobs", 0),
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_barber(session: AsyncSession, barber_id: int):
    query = delete(Barber).where(Barber.id == barber_id)
    await session.execute(query)
    await session.commit()


########### USER ###########

async def orm_add_user(session: AsyncSession, data: dict):
    try:
        user = User(
            user_name=data.get("user_name", ""),
            user_phone=data.get("user_phone"),
            telegram_id=data.get("telegram_id")
        )
        session.add(user)
        await session.commit()
    except Exception as e:
        print(f'Ошибка {e}')

async def orm_get_user(session: AsyncSession, telegram_id: int):
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalars().first()

########### ORDER ###########