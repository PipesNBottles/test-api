from libs.database import setup
from shift_service import settings
from libs.database import Base

engine, local_session = setup(
    uri=settings.database_uri,
    base=Base,
    pool_size=10,
    pool_timeout=30,
    pool_recycle=1800,
    max_overflow=100,
    pool_pre_ping=True,
)
