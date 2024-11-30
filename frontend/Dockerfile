# Use Node.js base image
FROM node:18

# Set working directory inside the container to /app.
WORKDIR /app

# Copy static files and directories from the public/
COPY public/ .

# Expose the frontend port
EXPOSE 8080

# Run a simple HTTP server
CMD ["npx", "http-server", "-p", "8080"]