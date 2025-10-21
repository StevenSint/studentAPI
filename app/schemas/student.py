from pydantic import BaseModel, EmailStr

# For creating a new student
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    grade: float
    major: str | None = None

# For updating a student
class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    grade: float | None = None
    major: str | None = None

# For API responses
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    grade: float
    major: str | None
    
    class Config:
        from_attributes = True  # Allows SQLAlchemy models to work