
# FROM python:3.9
# WORKDIR /code
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY ./app /code/app
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "run", "main:app", "--host", "0.0.0.0", "--port", "8000"]