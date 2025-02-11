FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only requirements
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY app ./app

# Set environment variables
ENV PYTHONPATH="/app:$PYTHONPATH"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
