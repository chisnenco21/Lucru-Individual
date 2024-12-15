FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install dependencies
# Using a placeholder requirements.txt for dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (adjust if needed)
EXPOSE 5000

# Command to run the application
CMD ["python", "financial_expert/run.py"]
