# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

EXPOSE 8000

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "mysite.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]