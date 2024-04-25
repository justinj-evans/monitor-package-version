FROM python:3.8-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

# Create a directory called src in the container
RUN mkdir src

# Copy the contents of the local src directory into the src directory in the container
COPY entrypoint.sh /app/
COPY src /app/src

# Set the entrypoint script to be executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh","/app/entrypoint.sh"]
