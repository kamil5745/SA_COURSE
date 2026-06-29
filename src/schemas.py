from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from models import Workload

class WorkersAddDTO(BaseModel):
    username: str

class WorkersDTO(WorkersAddDTO):
    id: int

class ResumesAddDTO(BaseModel):
    title: str
    compesation: Optional[int]
    worklaod: Workload
    worker_id: int

class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    update_at: datetime

class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"

class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]






















