from pydantic import BaseModel
from typing import List

class AutheniticityChecker(BaseModel):
    is_authentic: bool
    authenticity_score: float
    reasoning: str
    sources: List[str]

class AuthenticityError(BaseModel):
    error: str

class UserQuery(BaseModel):
    question: str