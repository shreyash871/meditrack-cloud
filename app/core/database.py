from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class Database:
    client: AsyncIOMotorClient | None = None


db = Database()


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        settings.mongodb_url,
        serverSelectionTimeoutMS=2000,
    )


async def close_mongo_connection():
    if db.client:
        db.client.close()


def get_database():
    return db.client[settings.database_name]


async def ping_database() -> bool:
    try:
        await db.client.admin.command("ping")
        return True
    except Exception:
        return False


async def create_indexes():
    """Enforce one booking per doctor per slot at the DB level."""
    database = get_database()
    await database.bookings.create_index(
        [("doctor_id", 1), ("slot", 1)],
        unique=True,
        name="uniq_doctor_slot",
    )
