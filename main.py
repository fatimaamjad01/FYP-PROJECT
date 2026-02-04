from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from schema import Query as StudentQuery, Mutation as StudentMutation, db as student_db  # Import your student Query, Mutation, and db
from AdminSchema import Query as AdminQuery, Mutation as AdminMutation, db as admin_db
from contextlib import asynccontextmanager
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

class Query(StudentQuery, AdminQuery):
    pass

class Mutation(StudentMutation, AdminMutation):
    pass

# Create the GraphQL schema using combined Query and Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Include the GraphQL route in the FastAPI app
app.include_router(graphql_app, prefix="/graphql")
