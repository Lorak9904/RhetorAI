FROM python:3.12.3-slim

WORKDIR /server_side

COPY . /server_side/

RUN apt-get update && apt-get install -y python3-venv

RUN python3 -m venv venv

RUN . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

CMD ["/server_side/venv/bin/python", "server.py"]
