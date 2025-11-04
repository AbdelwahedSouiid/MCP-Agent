from pydantic import BaseModel,Field
from app.enum.QueryType import QueryType
from typing import Optional

class Classification(BaseModel):
    Type: QueryType
    confidence: Optional[float] = Field(None, ge=0.5, le=1.0)
    

