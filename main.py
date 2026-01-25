from fastapi import FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()


app = FastAPI(lifespan=lifespan)


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    future_goal: Optional[str] = None


@app.get("/")
async def root():
    return {"msg": "working"}


@app.post("/students")
async def create_student(student: StudentCreate):
    try:
        new_student = await db.student.create(
            data={
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "password": student.password,
                "phone_number": student.phone_number,
                "gender": student.gender,
                "country": student.country,
                "city": student.city,
                "bio": student.bio,
                "profile_image": student.profile_image,
                "future_goal": student.future_goal,
            }
        )
        return new_student

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/students")
async def get_students():
    try:
        students = await db.student.find_many()
        return students

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
