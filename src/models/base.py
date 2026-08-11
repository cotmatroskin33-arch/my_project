import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeMeta, declarative_base

metadata = sa.MetaData()

Base: DeclarativeMeta = declarative_base(metadata=metadata)