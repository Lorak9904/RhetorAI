FROM python:3.12.3-slim

WORKDIR /server

COPY server/ /server/

RUN apt-get update && \
    apt-get install -y python3-venv && \
    python3 -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r requirements.txt

EXPOSE 8000

CMD ["/server/venv/bin/python", "main.py"]
