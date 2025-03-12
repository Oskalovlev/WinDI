# from passlib.context import CryptContext

# context = CryptContext(schemes=["bcrypt"])

# # Проверяем работу bcrypt
# password_hash = context.hash("mysecretpassword")
# print(password_hash)

from typing import Text
from sqlalchemy import create_engine

engine = create_engine('postgresql+asyncpg://postgres:postgres@localhost:5433/windi')

with engine.connect() as conn:
    conn.execute(Text("CREATE TABLE public.alembic_version (version_num VARCHAR(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))"))
