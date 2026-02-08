import strawberry
from prisma import Prisma
from typing import Optional
from fastapi import HTTPException
import typing
import bcrypt
import re
import datetime
import jwt
from datetime import timedelta
from InstructorSchema import Instructor as InstructorType


# Initialize Prisma client
db = Prisma()
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

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
@strawberry.type
class AdminLoginResponse:
    token: str
    user: "AdminUserInfo"
@strawberry.type
class AdminUserInfo:
    admin_id: int
    first_name: str
    last_name: str
    email: str
    role: str
    profile_image: Optional[str]

@strawberry.type
class AdminPaginatedResponse:
    admins: typing.List[Admin]
    total_count: int
    filtered_count: int


@strawberry.input
class AdminInput:
    first_name: str
    last_name: str
    email: str
    password: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    account_status: Optional[str] = None
    email_verified: Optional[bool] = None


@strawberry.type
class Query:
    @strawberry.field
    async def login_admin(self, email: str, password: str) -> AdminLoginResponse:
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
                    data={"last_login": datetime.datetime.now(datetime.timezone.utc).isoformat()}
                )
            except Exception:
                raise HTTPException(status_code=400, detail=f"Error updating last_login:{str(e)}")
            
            # Create JWT token with basic admin information and role
            token_data = {
                "sub": str(admin.admin_id),
                "email": admin.email,
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "role": "admin"  # Added role field
            }
            access_token = create_access_token(data=token_data)
            
            # Create admin user info object
            admin_user_info = AdminUserInfo(
                admin_id=admin.admin_id,
                first_name=admin.first_name,
                last_name=admin.last_name,
                email=admin.email,
                role="admin",  # Added role field
                profile_image=admin.profile_image
            )
            
            return AdminLoginResponse(token=access_token, user=admin_user_info)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @strawberry.field
    async def list_admins_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "admin_id",
        sort_order: str = "asc",
        search: typing.Optional[str] = None,
    ) -> AdminPaginatedResponse:
        """
        Get paginated list of admins with optional search filter on name or email
        """
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        skip = (page - 1) * per_page

        # Validate sort field
        allowed_sort_fields = {
            "admin_id",
            "first_name",
            "last_name",
            "email",
            "account_status",
            "created_at",
            "updated_at",
        }
        field = sort_field if sort_field in allowed_sort_fields else "admin_id"
        direction = sort_order.lower() if sort_order.lower() in {"asc", "desc"} else "asc"
        order: typing.Optional[dict] = {field: direction}

        try:
            # Build where clause for search
            where_clause = {}
            if search:
                where_clause = {
                    "OR": [
                        {"first_name": {"contains": search, "mode": "insensitive"}},
                        {"last_name": {"contains": search, "mode": "insensitive"}},
                        {"email": {"contains": search, "mode": "insensitive"}},
                    ]
                }

            # Get total count (without filters)
            total_count = await db.admin.count()

            # Get filtered count (with search filter)
            filtered_count = await db.admin.count(where=where_clause if where_clause else None)

            # Get paginated admins
            admins = await db.admin.find_many(
                where=where_clause if where_clause else None,
                skip=skip,
                take=per_page,
                order=order,
            )

            return AdminPaginatedResponse(
                admins=admins,
                total_count=total_count,
                filtered_count=filtered_count
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @strawberry.field
    async def get_admin(self, admin_id: int) -> Admin:
        """
        Get a single admin by ID
        """
        try:
            admin = await db.admin.find_unique(where={"admin_id": admin_id})
            if not admin:
                raise HTTPException(status_code=404, detail=f"Admin with ID {admin_id} not found")
            return admin
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    @strawberry.field
    async def list_instructors(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "instructor_id",
        sort_order: str = "asc",
    ) -> typing.List[InstructorType]:
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 10
        skip = (page - 1) * per_page

        allowed_sort_fields = {
            "instructor_id",
            "first_name",
            "last_name",
            "email",
            "account_status",
            "created_at",
            "updated_at",
        }
        field = sort_field if sort_field in allowed_sort_fields else "instructor_id"
        direction = sort_order.lower() if sort_order.lower() in {"asc", "desc"} else "asc"
        order: typing.Optional[dict] = {field: direction}

        try:
            instructors = await db.instructor.find_many(
                skip=skip,
                take=per_page,
                order=order,
            )
            return instructors
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")




@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register_admin(self, input: AdminInput) -> Admin:
        try:
            # Validate email
            validate_email(input.email)
            
            # Ensure password is provided for registration
            if not input.password or not input.password.strip():
                raise ValueError("Password is required for registration")
            
            # Validate password strength
            validate_password(input.password)
            
            # Check if email already exists
            existing = await db.admin.find_unique(where={"email": input.email})
            if existing:
                raise ValueError(f"Email {input.email} is already registered")
            
            # Hash the password
            hashed = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt())
            
            # Create the admin
            admin = await db.admin.create(
                data={
                    "first_name": input.first_name,
                    "last_name": input.last_name,
                    "email": input.email,
                    "password": hashed.decode('utf-8'),
                    "phone_number": input.phone_number if input.phone_number else None,
                    "profile_image": input.profile_image,
                    "account_status": input.account_status if input.account_status else "active",
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
            # Check if admin exists
            existing = await db.admin.find_unique(where={"admin_id": admin_id})
            if not existing:
                raise HTTPException(status_code=404, detail=f"Admin with ID {admin_id} not found")
            
            # Validate email
            validate_email(input.email)
            
            # Build update data dictionary dynamically
            update_data = {
                "first_name": input.first_name,
                "last_name": input.last_name,
                "email": input.email,
            }
            
            # Only update phone_number if provided
            if input.phone_number is not None:
                update_data["phone_number"] = input.phone_number
            
            # Only update profile_image if provided
            if input.profile_image is not None:
                update_data["profile_image"] = input.profile_image
            
            # Only update account_status if provided
            if input.account_status is not None:
                update_data["account_status"] = input.account_status
            
            # Only update email_verified if provided
            if input.email_verified is not None:
                update_data["email_verified"] = input.email_verified
            
            # Hash and update password only if provided and not empty
            if input.password and input.password.strip():
                validate_password(input.password)
                hashed = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_data["password"] = hashed
            
            # Perform the update
            updated = await db.admin.update(
                where={"admin_id": admin_id},
                data=update_data
            )
            return updated
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
