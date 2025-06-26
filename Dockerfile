FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install pytest

CMD ["python", "-m", "unittest", "discover"]
