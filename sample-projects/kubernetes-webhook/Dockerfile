# Use a lightweight Python image
FROM python:3.10-alpine

RUN apt-get update && apt-get install -y \
    curl \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY app.py .

# Copy the CA Cert to the /etc/ssl/certs so that Cert signed by  unknown authority issue may not come.
COPY ssl-generate/ca.crt /etc/ssl/certs/ca-bundle.pem

RUN update-ca-certificates

# Expose the port
EXPOSE 5000


# Run the application
CMD ["python", "app.py"]