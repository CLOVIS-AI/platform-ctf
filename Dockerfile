FROM python:alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD [ "/app/start.sh" ]

# Dependencies:
# - terraform: remote VM management
# - gcc, make…: compile Python dependencies
# - curl, OpenSSH…: communicate with the VMs and other machines
RUN apk add --no-cache \
	terraform bash \
    gcc make build-base libffi-dev musl-dev \
    curl openssh openssl openssl-dev \
    py3-paramiko python3-dev

# Copy only the requirements file, because it doesn't change often
# The other files will be copied later, because they change often and are not required to install dependencies
# (which don't change often either)
COPY web/requirements.txt /app/requirements.txt
RUN cd /app \
 && python3 -m venv venv \
 && . venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy all Python, templates, static files, etc
COPY web /app

# Include the challenges in the container
COPY challenges /app/challenges
