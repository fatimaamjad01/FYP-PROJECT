from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from schema import Query, Mutation, db  # Import your Query, Mutation, and db (Prisma)
from contextlib import asynccontextmanager
# Use the lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database when the app starts
    await db.connect()

    # Disconnect from the database when the app shuts down
    yield

    await db.disconnect()


app = FastAPI(lifespan=lifespan)

# Create the GraphQL schema using Query and Mutation
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the GraphQL router
graphql_app = GraphQLRouter(schema)

# Include the GraphQL route in the FastAPI app
app.include_router(graphql_app, prefix="/graphql")
