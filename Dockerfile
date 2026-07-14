# Use the official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Copy requirements and install dependencies from the development phase directory
COPY "5. Project Development Phase/requirements.txt" /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application files from the development phase directory
COPY "5. Project Development Phase/" /code/

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
