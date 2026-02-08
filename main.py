from fastapi import FastAPI, Depends, HTTPException, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware  
from strawberry.fastapi import GraphQLRouter
import strawberry
import jwt
from StudentSchema import Query as StudentQuery, Mutation as StudentMutation, db as student_db, Student as StudentType, StudentInput as StudentInputType, LoginResponse as StudentLoginResponse, SECRET_KEY, ALGORITHM
from AdminSchema import (
    Query as AdminQuery, 
    Mutation as AdminMutation, 
    db as admin_db, 
    Admin as AdminType, 
    AdminInput as AdminInputType,
    AdminLoginResponse,
    AdminPaginatedResponse
)
from InstructorSchema import (
    Query as InstructorQuery,
    Mutation as InstructorMutation,
    db as instructor_db,
    Instructor as InstructorType,
    InstructorInput as InstructorInputType,
    InstructorLoginResponse,
    Course as CourseType,
    CourseInput as CourseInputType,
)
from contextlib import asynccontextmanager
import typing

security = HTTPBearer()

# Token verification function
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Use the lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database when the app starts
    await student_db.connect()
    await admin_db.connect()
    await instructor_db.connect()

    # Disconnect from the database when the app shuts down
    yield

    await student_db.disconnect()
    await admin_db.disconnect()
    await instructor_db.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Your React app origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@strawberry.type
class Query:
    # Student queries
    @strawberry.field
    async def get_student(self, id: strawberry.ID) -> StudentType:
        return await StudentQuery().get_student(id)

    @strawberry.field
    async def list_students(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "id",
        sort_order: str = "asc",
    ) -> typing.List[StudentType]:
        return await StudentQuery().list_students(page=page, per_page=per_page, sort_field=sort_field, sort_order=sort_order)

    @strawberry.field
    async def login_student(self, email: str, password: str) -> StudentLoginResponse:
        return await StudentQuery().login_student(email, password)

    # Admin queries
    @strawberry.field
    async def login_admin(self, email: str, password: str) -> AdminLoginResponse:
        return await AdminQuery().login_admin(email, password)

    @strawberry.field
    async def list_admins_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "admin_id",
        sort_order: str = "asc",
        search: typing.Optional[str] = None,
    ) -> AdminPaginatedResponse:
        return await AdminQuery().list_admins_paginated(
            page=page,
            per_page=per_page,
            sort_field=sort_field,
            sort_order=sort_order,
            search=search
        )

    @strawberry.field
    async def get_admin(self, admin_id: int) -> AdminType:
        return await AdminQuery().get_admin(admin_id)

    @strawberry.field
    async def list_instructors(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "instructor_id",
        sort_order: str = "asc",
    ) -> typing.List[InstructorType]:
        return await AdminQuery().list_instructors(
            page=page,
            per_page=per_page,
            sort_field=sort_field,
            sort_order=sort_order,
        )

    # Instructor queries
    @strawberry.field
    async def login_instructor(self, email: str, password: str) -> InstructorLoginResponse:
        return await InstructorQuery().login_instructor(email, password)

    @strawberry.field
    async def list_courses(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_field: str = "course_id",
        sort_order: str = "asc",
    ) -> typing.List[CourseType]:
        return await InstructorQuery().list_courses(
            page=page,
            per_page=per_page,
            sort_field=sort_field,
            sort_order=sort_order,
        )

@strawberry.type
class Mutation:
    # Student mutations
    @strawberry.mutation
    async def register_student(self, input: StudentInputType) -> StudentType:
        return await StudentMutation().register_student(input)

    @strawberry.mutation
    async def update_student(self, id: int, input: StudentInputType) -> StudentType:
        return await StudentMutation().update_student(id, input)

    # Admin mutations
    @strawberry.mutation
    async def register_admin(self, input: AdminInputType) -> AdminType:
        return await AdminMutation().register_admin(input)

    @strawberry.mutation
    async def update_admin(self, admin_id: int, input: AdminInputType) -> AdminType:
        return await AdminMutation().update_admin(admin_id, input)

    # Instructor mutations
    @strawberry.mutation
    async def register_instructor(self, input: InstructorInputType) -> InstructorType:
        return await InstructorMutation().register_instructor(input)

    @strawberry.mutation
    async def update_instructor(self, instructor_id: int, input: InstructorInputType) -> InstructorType:
        return await InstructorMutation().update_instructor(instructor_id, input)

    @strawberry.mutation
    async def create_course(self, input: CourseInputType) -> CourseType:
        return await InstructorMutation().create_course(input)

    @strawberry.mutation
    async def update_course(self, course_id: int, input: CourseInputType) -> CourseType:
        return await InstructorMutation().update_course(course_id, input)

# Create the GraphQL schema using combined Query and Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Include the GraphQL route in the FastAPI app
app.include_router(graphql_app, prefix="/graphql")

# Optional: Add a protected endpoint example
@app.get("/protected")
async def protected_route(token_data: dict = Depends(verify_token)):
    return {
        "message": "This is a protected route",
        "user": token_data
    }