from pydantic import BaseModel
from typing import Optional


class GenerationGETResult(BaseModel):
    file_path: str


class GenerationGETStatus(BaseModel):
    task_id: str
    state: str
    status: str
    result: Optional[GenerationGETResult]
