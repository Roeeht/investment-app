from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import backend_api
from db.database import Base, engine
from db import models


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(backend_api.router, prefix="/api")


# Add CORS middleware
origins = [
    "http://localhost:3000",  # React app URL
    "http://127.0.0.1:3000",  # React app URL (for different localhost access)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#health check endpoint
@app.get("/")
def read_root():
    return {"message": "Investment App API"}