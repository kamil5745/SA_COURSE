import datetime

from typing import Annotated
from sqlalchemy import Column, Integer, MetaData, ForeignKey, String, Table, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"), 
        onupdate=datetime.datetime.utcnow)]


class WorkersOrm(Base):
    __tablename__ = 'workers'

    worker_id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["ResumesOrm"]] = relationship(back_populates="worker")

class Workload(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'

class ResumesOrm(Base):
    __tablename__ = 'resumes'

    resumes_id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.worker_id', ondelete='CASCADE'))
    created_at: Mapped[created_at] 
    updated_at: Mapped[updated_at]

    worker: Mapped["WorkersOrm"] = relationship(back_populates="resumes")

    repr_cols_num = 4
    repr_cols = ("created_at",)



metadata_obj = MetaData()

workers_table  = Table(
    'workers',
    metadata_obj,
    Column('worker_id', Integer, primary_key=True),
    Column('username', String),
)