from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from strawberry.fastapi import GraphQLRouter
import strawberry
import jwt
from schema import Query as StudentQuery, Mutation as StudentMutation, db as student_db, Student as StudentType, StudentInput as StudentInputType, LoginResponse as StudentLoginResponse, SECRET_KEY, ALGORITHM
from AdminSchema import (
    Query as AdminQuery, 
    Mutation as AdminMutation, 
    db as admin_db, 
    Admin as AdminType, 
    AdminInput as AdminInputType,
    AdminLoginResponse
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

    # Disconnect from the database when the app shuts down
    yield

    await student_db.disconnect()
    await admin_db.disconnect()


app = FastAPI(lifespan=lifespan)

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

    # Admin queries
    @strawberry.field
    async def login_admin(self, email: str, password: str) -> AdminLoginResponse:
        return await AdminQuery().login_admin(email, password)

@strawberry.type
class Mutation:
    # Student mutations
    @strawberry.mutation
    async def register_student(self, input: StudentInputType) -> StudentType:
        return await StudentMutation().register_student(input)

    @strawberry.mutation
    async def update_student(self, id: int, input: StudentInputType) -> StudentType:
        return await StudentMutation().update_student(id, input)

    @strawberry.mutation
    async def login_student(self, email: str, password: str) -> StudentLoginResponse:
        return await StudentMutation().login_student(email, password)

    # Admin mutations
    @strawberry.mutation
    async def register_admin(self, input: AdminInputType) -> AdminType:
        return await AdminMutation().register_admin(input)

    @strawberry.mutation
    async def update_admin(self, admin_id: int, input: AdminInputType) -> AdminType:
        return await AdminMutation().update_admin(admin_id, input)

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