FROM selenium/standalone-chrome:latest

USER root

# Set working directory
WORKDIR /app

# Install system dependencies including pyenv dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    git \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pyenv
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Copy dependency files first
COPY pyproject.toml poetry.lock* ./

# Install pyenv, Python 3.12, and dependencies in a single RUN to maintain environment
RUN curl https://pyenv.run | bash && \
    export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH" && \
    eval "$(pyenv init -)" && \
    pyenv install 3.12.8 && \
    pyenv global 3.12.8 && \
    pyenv rehash && \
    rm -f /usr/bin/python3 /usr/bin/pip3 /usr/bin/python /usr/bin/pip && \
    ln -s $PYENV_ROOT/shims/python3 /usr/bin/python3 && \
    ln -s $PYENV_ROOT/shims/python /usr/bin/python && \
    ln -s $PYENV_ROOT/shims/pip3 /usr/bin/pip3 && \
    ln -s $PYENV_ROOT/shims/pip /usr/bin/pip && \
    python --version && \
    which python && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy application code (including .streamlit config)
COPY . .

# Copy and make database initialization script executable
COPY init_db.sh /app/init_db.sh
RUN chmod +x /app/init_db.sh

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run database initialization and then start Streamlit
ENTRYPOINT ["/bin/bash", "-c", "/app/init_db.sh && streamlit run src/main.py"]
