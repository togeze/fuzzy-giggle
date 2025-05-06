from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.database.unit_of_work import UnitOfWork

DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

def get_uow():
    return UnitOfWork(async_session)