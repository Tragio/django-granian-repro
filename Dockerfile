# Use an official Python runtime as a parent image
FROM arm64v8/python:3.12.8-slim-bookworm

WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install uv package manager
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

# Place executables in the environment at the front of the path
ENV PATH="/code/.venv/bin:$PATH"

EXPOSE 8000

# Add healthcheck configuration
HEALTHCHECK --interval=5s --timeout=10s --start-period=5s --retries=100 \
    CMD curl -f http://localhost:8000/up || exit 1

CMD ["uv", "run", "granian", "main.asgi:application", "--host", "0.0.0.0", "--port", "8000"]