FROM python:3.12-slim

WORKDIR /src

COPY src/ ./src
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/src
ENV FLASK_APP=sentry:create_app()
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--debug"]
