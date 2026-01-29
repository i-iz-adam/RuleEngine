FROM python:3.12-slim

WORKDIR /app

# Copy everything that pip needs to build the package
COPY pyproject.toml .
COPY src/ src/
COPY README.md .
RUN pip install --upgrade pip && pip install -e .[dev]

# Copy tests separately
COPY tests/ tests/

# Default command: run tests
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q"]
