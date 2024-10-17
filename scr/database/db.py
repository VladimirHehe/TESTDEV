from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import (DB_USER, DB_PASS, DB_NAME, DB_PORT, DB_HOST)

DB = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    url=DB,
    echo=True,
    pool_size=5,
    max_overflow=10,

)

Session_factory = sessionmaker(engine)
