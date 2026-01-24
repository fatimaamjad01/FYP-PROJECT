from fastapi import FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel

app = FastAPI()
db = Prisma()


class StudentCreate(BaseModel):
    name: str
    email: str


@app.get("/")
async def root():
    return {"msg": "working"}


@app.post("/students")
async def create_student(student: StudentCreate):
    try:
        if not db.is_connected():
            await db.connect()

        new_student = await db.student.create(
            data={
                "name": student.name,
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
        if not db.is_connected():
            await db.connect()

        students = await db.student.find_many()
        return students

    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
