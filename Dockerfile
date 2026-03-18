# 1. Start with a lightweight Linux environment that has Python 3.10 pre-installed
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system-level dependencies (MUMmer and MMseqs2)
RUN apt-get update && apt-get install -y \
    mummer \
    mmseqs2 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the entire PySyntenyViz project (including pyproject.toml and source code)
COPY . .

# 5. Install the package and its dependencies via pip
# This reads pyproject.toml and registers the 'synviz' console script
RUN pip install --no-cache-dir .

# 6. Set the newly created console script as the entrypoint
ENTRYPOINT ["pysyntenyviz"]