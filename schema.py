import strawberry
from prisma import Prisma
from typing import Optional
import typing
import bcrypt

# Initialize Prisma client
db = Prisma()



@strawberry.type
class Student:
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    dob: Optional[str]
    gender: Optional[str]
    country: Optional[str]
    city: Optional[str]
    bio: Optional[str]
    profile_image: Optional[str]
    future_goal: Optional[str]
    password: str
    account_status: str
    email_verified: bool
    last_login: Optional[str]
    password_last_change: Optional[str]
    created_at: str
    updated_at: str
    


@strawberry.type
class Query:
    @strawberry.field
    async def get_student(self, id: strawberry.ID) -> Student:
        student = await db.student.find_unique(where={"id": id})
        
        if student is None:
            raise Exception(f"Student with ID {id} not found")
    
        return student

    @strawberry.field
    async def list_students(self) -> typing.List[Student]:
        try:
            students = await db.student.find_many()
            return students
        except Exception as e:
            print("DB ERROR:", e)
            raise Exception(f"An error occurred: {str(e)}")

@strawberry.input
class StudentInput:
    first_name: str
    last_name: str
    email: str
    password: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_student(self, id: int, input: StudentInput) -> Student:
        updated_student = await db.student.update(
            where={"id": id},
            data={
                "first_name": input.first_name,
                "last_name": input.last_name,
                "email": input.email
                
            }
                )
        return updated_student
        

    @strawberry.mutation
    async def register_student(self, input: StudentInput) -> Student:
        try:
            # Validate password (minimum 8 characters as an example)
            if len(input.password) < 8:
                raise ValueError("Password must be at least 8 characters long")

            hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            existing_student = await db.student.find_unique(where={"email": input.email})
            if existing_student:
                raise ValueError(f"Email {input.email} is already registered")

            registered_student  = await db.student.create(
                data={
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "email": input.email,
                    "password": hashed_password.decode('utf-8')
                }
            )
            print(registered_student)
            return registered_student
        except ValueError as e:
            # Handle validation errors (like password length or duplicate email)
            raise Exception(f"Validation error: {str(e)}")
        except Exception as e:
            # Catch any other errors
            raise Exception(f"An error occurred: {str(e)}")
