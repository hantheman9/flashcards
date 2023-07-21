FROM python:3.7

WORKDIR /backend

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt /backend/
COPY requirements-dev.txt /backend/

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

# Copy the contents from your host to your current location.
COPY . /backend

# Specify the command to run
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 app.app:application
