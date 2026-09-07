from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_read_session, get_write_session

ReadSessionDep = Annotated[AsyncSession, Depends(get_read_session)]
WriteSessionDep = Annotated[AsyncSession, Depends(get_write_session)]
