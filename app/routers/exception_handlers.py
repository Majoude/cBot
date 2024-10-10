# Importing necessary libraries

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTPException.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The raised HTTPException.

    Returns:
        JSONResponse: A custom JSON response for HTTP exceptions.
    """
    logging.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """
    Custom handler for generic exceptions.

    Args:
        request (Request): The incoming request.
        exc (Exception): The raised exception.

    Returns:
        JSONResponse: A custom JSON response for generic exceptions.
    """
    logging.error(f"An error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )
