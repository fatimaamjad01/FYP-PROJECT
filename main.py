from fastapi import FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from contextlib import asynccontextmanager

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
    email: str


@app.get("/")
async def root():
    return {"msg": "working"}


@app.post("/students")
async def create_student(student: StudentCreate):
    try:
        new_student = await db.student.create(
            data={
                "first_name": student.first_name,
                "email": student.email,
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
