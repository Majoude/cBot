# Use an official Python 3.9 slim image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /cbot/app

# Copy the current directory contents into the container at /cbot
COPY . /cbot

# Install any dependencies listed in requirements.txt

COPY ./requirements.txt /cbot/requirements.txt
RUN pip install --no-cache-dir -r /cbot/requirements.txt

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH="${PYTHONPATH}:/cbot/app"

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




# FROM python:3.9
# WORKDIR /code
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY ./cBot/app /code/app
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# FROM python:3.9-slim
# WORKDIR /app_code
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY ./app /app_code
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]