from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    age: Mapped[int]
    course: Mapped[str] = mapped_column(String(100), index=True)
    semester: Mapped[int]
    department: Mapped[str] = mapped_column(String(100), index=True)
