FROM python:3.11-slim

WORKDIR /app

# Install uv, then use uv to install dependencies
COPY pyproject.toml .
RUN pip install uv
RUN uv install

# Copy the Django project
COPY . .

# Expose the port that Django will run on
EXPOSE 8000

# Run migrations and start the server
CMD ["uv", "python", "manage.py", "migrate", "&&", "uv", "python", "manage.py", "runserver", "0.0.0.0:8000"]
