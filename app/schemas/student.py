from pydantic import BaseModel, ConfigDict, EmailStr, Field

class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    age: int = Field(ge=1, le=100)
    course: str = Field(min_length=1, max_length=100)
    semester: int = Field(ge=1, le=12)
    department: str = Field(min_length=1, max_length=100)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=1, le=100)
    course: str | None = Field(default=None, min_length=1, max_length=100)
    semester: int | None = Field(default=None, ge=1, le=12)
    department: str | None = Field(default=None, min_length=1, max_length=100)

class StudentRead(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
