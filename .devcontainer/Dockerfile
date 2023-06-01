FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Prevents python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turn off buffering for easier contianer logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements, Upgrade pip && install modules
COPY requirements.txt .
RUN python -m pip install --no-cache-dir install --upgrade pip && \
    python -m pip install --no-cache-dir install -r requirements.txt

WORKDIR /bernardshop
COPY . /bernardshop

# During debugging, this entry point will be overridden
CMD ['python', 'manage.py runserver']
