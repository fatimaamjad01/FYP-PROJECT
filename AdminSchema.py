import strawberry
from prisma import Prisma
from typing import Optional
from fastapi import HTTPException
import bcrypt
import re
import datetime


# Initialize Prisma client
db = Prisma()

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("Password must contain at least one letter")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")

def validate_email(email: str):
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")


@strawberry.type
class Admin:
    admin_id: int
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str]
    profile_image: Optional[str]
    account_status: Optional[str]
    email_verified: bool
    last_login: Optional[str]
    password_last_change: Optional[str]
    created_at: str
    updated_at: str


@strawberry.input
class AdminInput:
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    account_status: Optional[str] = None
    email_verified: Optional[bool] = None


@strawberry.type
class Query:
    @strawberry.field
    async def login_admin(self, email: str, password: str) -> Admin:
        try:
            admin = await db.admin.find_unique(where={"email": email})
            if not admin:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            if not bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
                raise HTTPException(status_code=401, detail="Invalid email or password")
            # update last_login
            try:
                await db.admin.update(
                    where={"admin_id": admin.admin_id},
                    data={"last_login": datetime.utcnow().isoformat()}
                )
            except Exception:
                raise HTTPException(status_code=400, detail=f"Error updating last_login:{str(e)}")
            return admin
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register_admin(self, input: AdminInput) -> Admin:
        try:
            validate_email(input.email)
            validate_password(input.password)
            existing = await db.admin.find_unique(where={"email": input.email})
            if existing:
                raise ValueError(f"Email {input.email} is already registered")
            hashed = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            admin = await db.admin.create(
                data={
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "email": input.email,
                    "password": hashed.decode('utf-8'),
                    "phone_number": input.phone_number,
                    "profile_image": input.profile_image,
                    "account_status": input.account_status,
                    "email_verified": input.email_verified if input.email_verified is not None else False,
                }
            )
            return admin
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @strawberry.mutation
    async def update_admin(self, admin_id: int, input: AdminInput) -> Admin:
        try:
            validate_email(input.email)
            # hash password if provided
            if input.password:
                validate_password(input.password)
                hashed = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else:
                hashed = None
            existing = await db.admin.find_unique(where={"admin_id": admin_id})
            if not existing:
                raise HTTPException(status_code=404, detail=f"Admin with ID {admin_id} not found")
            updated = await db.admin.update(
                where={"admin_id": admin_id},
                data={
                    "first_name": input.first_name if hasattr(input, 'first_name') else existing.first_name,
                    "last_name": input.last_name if hasattr(input, 'last_name') else existing.last_name,
                    "email": input.email if hasattr(input, 'email') else existing.email,
                    "phone_number": input.phone_number if hasattr(input, 'phone_number') else existing.phone_number,
                    "profile_image": input.profile_image if hasattr(input, 'profile_image') else existing.profile_image,
                    "email_verified": input.email_verified if hasattr(input, 'email_verified') else existing.email_verified,
                    "account_status": input.account_status if hasattr(input, 'account_status') else existing.account_status,
                    "password": hashed if hashed else existing.password,
                }
            )
            return updated
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
