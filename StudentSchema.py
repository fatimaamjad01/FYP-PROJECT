import  strawberry
from prisma import Prisma
from typing import Optional
from fastapi import HTTPException
import typing
import bcrypt
import re
import datetime
import jwt
from datetime import timedelta


# Initialize Prisma client
db = Prisma()
# JWT Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"  # Change this to a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    # You can add more complex rules for password strength here, such as checking for numbers, special chars, etc.
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Password must contain at least one letter")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")
    # Email validation function
def validate_email(email: str):
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    


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
class LoginResponse:
    token: str
    user: "UserInfo"

@strawberry.type
class UserInfo:
    id: int
    first_name: str
    last_name: str
    email: str
    role: str
    profile_image: Optional[str]
    


@strawberry.type
class Query:
    @strawberry.field
    async def get_student(self, id: strawberry.ID) -> Student:
        student = await db.student.find_unique(where={"id": int(id)})
        
        if student is None:
            raise Exception(f"Student with ID {id} not found")
        
        return student

    @strawberry.field
    async def list_students(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "id",
        sort_order: str = "asc",
    ) -> typing.List[Student]:
        
        # Normalize pagination parameters to sensible defaults
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        skip = (page - 1) * per_page

        # Define allowed fields for sorting to prevent arbitrary SQL injection
        allowed_sort_fields = {
            "id",
            "first_name",
            "last_name",
            "email",
            "created_at",
            "updated_at",
        }
        # Fallback to 'id' if the provided field isn't valid
        field = sort_field if sort_field in allowed_sort_fields else "id"
        direction = sort_order.lower() if sort_order.lower() in {"asc", "desc"} else "asc"

        # Compose the order argument for Prisma. If no sorting is desired, omit
        order: typing.Optional[dict] = {field: direction}

        try:
            students = await db.student.find_many(
                skip=skip,
                take=per_page,
                order=order,
            )
            return students
        except Exception as e:
            # Bubble up a generic error message; log internal details for debugging
            print("DB ERROR:", e)
            raise Exception(f"An error occurred: {str(e)}")

@strawberry.input
class StudentInput:
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None   
    city: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    future_goal: Optional[str] = None



@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_student(self, id: int, input: StudentInput) -> Student:
        try:
            validate_email(input.email)
            # Validate password format (only validate if password is provided)
            if input.password:
                validate_password(input.password)
                hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            else:
                hashed_password = None
            # Fetch the existing student to get the current password if not updating
            existing_student = await db.student.find_unique(where={"id": id})
            if not existing_student:
                raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        updated_student = await db.student.update(
            where={"id": id},
            data={
                "first_name": input.first_name if hasattr(input, "first_name") else existing_student.first_name,
                "last_name": input.last_name if hasattr(input, "last_name") else existing_student.last_name,
                "email": input.email if hasattr(input, "email") else existing_student.email,
                "dob": input.dob if hasattr(input, "dob") else existing_student.dob,
                "phone_number": input.phone_number if hasattr(input, "phone_number") else existing_student.phone_number,
                "gender": input.gender if hasattr(input, "gender") else existing_student.gender,
                "country": input.country if hasattr(input, "country") else existing_student.country,
                "city": input.city if hasattr(input, "city") else existing_student.city,
                "bio": input.bio if hasattr(input, "bio") else existing_student.bio,
                "profile_image": input.profile_image if hasattr(input, "profile_image") else existing_student.profile_image,
                "future_goal": input.future_goal if hasattr(input, "future_goal") else existing_student.future_goal,
                "password": hashed_password.decode('utf-8') if hashed_password else existing_student.password,
        }
                )
        return updated_student
        

    @strawberry.mutation
    async def register_student(self, input: StudentInput) -> Student:
        try:
            # Validate password (minimum 8 characters as an example)
            validate_password(input.password)
            validate_email(input.email)

            hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            existing_student = await db.student.find_unique(where={"email": input.email})
            if existing_student:
                raise ValueError(f"Email {input.email} is already registered")

            registered_student  = await db.student.create(
                data={
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "email": input.email,
                    "password": hashed_password.decode('utf-8'),
                }
            )
            print(registered_student)
            return registered_student
        except ValueError as e:
            # Handle validation errors (like password length or duplicate email)
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        except Exception as e:
            # Catch any other errors
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    @strawberry.mutation
    async def login_student(self, email: str, password: str) -> LoginResponse:
        try:
            student = await db.student.find_unique(where={"email": email})
            if not student:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), student.password.encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid email or password")
            # Update last_login timestamp (best-effort, ignore update errors)
            try:
                await db.student.update(
                    where={"id": student.id},
                    data={"last_login": datetime.datetime.now(datetime.timezone.utc).isoformat()}
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error updating last_login:{str(e)}")
            
            token_data = {
                "sub": str(student.id),
                "email": student.email,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "role": "student" 
            }
            access_token = create_access_token(data=token_data)
            
            # Create user info object
            user_info = UserInfo(
                id=student.id,
                first_name=student.first_name,
                last_name=student.last_name,
                email=student.email,
                role="student", 
                profile_image=student.profile_image
            )
            
            return LoginResponse(token=access_token, user=user_info)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")