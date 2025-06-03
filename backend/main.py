from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import backend_api
from db.database import engine
from db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(backend_api.router)


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
