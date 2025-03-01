# Use a lightweight Python image
FROM python:3.9-slim-buster

# Create a working directory inside the container
WORKDIR /app

# With psycopg2-binary, you usually don't need libpq-dev/gcc, but if you run into issues:
# RUN apt-get update && apt-get install -y libpq-dev gcc

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container (Copies the rest of your project into /app.)
COPY . .

# Expose the port Flask uses
EXPOSE 5000

# Run Flask
CMD ["python", "app.py"]
