FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (can also be set in Render dashboard)
ENV GROQ_API_KEY=""
ENV API_KEY="MY_SUPER_SECRET"

# Expose FastAPI port
EXPOSE 8080

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
