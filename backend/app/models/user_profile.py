from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    email: EmailStr
    phone: str
    education: List[str]
    experience: List[str]
    skills: List[str]
    certifications: Optional[List[str]] = []
