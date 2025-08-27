FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies with optimizations
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir wheel setuptools && \
    # Install dlib separately with optimizations
    pip3 install --no-cache-dir dlib --no-build-isolation && \
    # Install other dependencies
    pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY app.py ./
COPY multi_agent_framework.py ./
COPY perception_agent.py ./
COPY decision_agent.py ./
COPY action_agent.py ./
COPY example.py ./
COPY test.py ./
COPY gaze_tracking/ ./gaze_tracking/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Start command
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
