# Us python base images
FROM python:3.10

# Set working directory  directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copies all files and directories from the backend/ folder into the /app directory in the container.
COPY . .

# Expose the backend port in Docker
EXPOSE 8001

# Run the application CMD [...]: Specifies the default command 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]