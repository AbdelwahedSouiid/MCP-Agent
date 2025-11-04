from pydantic import BaseModel
from typing import List

class Segment(BaseModel):
    start: float
    end: float
    text: str

class TranscriptionResponse(BaseModel):
    language: str
    language_probability: float
    segments: List[Segment]
