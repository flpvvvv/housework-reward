FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

# Expose the port that Django will run on
EXPOSE 8000

# Run migrations and start the server
CMD ["uv","run", "manage.py", "runserver", "0.0.0.0:8000"]
