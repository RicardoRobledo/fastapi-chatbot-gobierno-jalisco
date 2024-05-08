from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


__author__ = "Ricardo Robledo"
__version__ = "0.1"
__all__ = ['Procedure']


class Base(DeclarativeBase):
    pass


class Procedure(Base):

    __tablename__ = "procedures"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    file_name: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"Procedure(id={self.id}, name={self.name}, file_name={self.file_name})"
