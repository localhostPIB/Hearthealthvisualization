# syntax=docker/dockerfile:1

# Stage 1 – Build
FROM python:3.11 as build
ENV VENV=/opt/venv
RUN python -m venv $VENV
ENV PATH="$VENV/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Stage 2 – Runtime
FROM python:3.11-slim AS runtime
ENV VENV=/opt/venv
ENV PATH="$VENV/bin:$PATH"

WORKDIR /app
COPY --from=build $VENV $VENV
COPY . .
