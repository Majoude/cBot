# Importing necessary libraries

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import client, user, chat, management
from routers.exception_handlers import custom_http_exception_handler, generic_exception_handler

# Initialize FastAPI app

app = FastAPI(
    title="cBot API",
    description="API for managing chat bot operations",
    version="1.0.0",
)

# CORS settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Exception handlers

app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers

app.include_router(client.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(management.router)

# Run the application using Uvicorn server

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 
