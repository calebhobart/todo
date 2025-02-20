from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, todos, lists

app = FastAPI(
    title="Todo API",
    description="A FastAPI backend for the Todo application",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",  # React/Next.js frontend - this does not exist yet
    "http://localhost:8000",  # FastAPI docs
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    todos.router,
    prefix="/lists/{list_id}/todos",
    tags=["Todos"]
)

# Add a new router for todo operations that don't need list_id
app.include_router(
    todos.todo_router,  # New router for individual todo operations
    prefix="/todos",
    tags=["Todos"]
)

app.include_router(
    lists.router,
    prefix="/lists",
    tags=["Lists"]
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def read_root():
    return {"status": "healthy", "message": "Todo API is running"} 