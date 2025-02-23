FROM python:3.12.3-slim

# Set the working directory to /server_side
WORKDIR /server_side

# Copy the entire project directory into the container
COPY server_side/ /server_side/

# Create the virtual environment and install dependencies in one step
RUN apt-get update && \
    apt-get install -y python3-venv && \
    python3 -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run main.py using the virtual environment's Python
CMD ["/server_side/venv/bin/python", "main.py"]
