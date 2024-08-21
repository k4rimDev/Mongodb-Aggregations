# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /code
ENV VENV_PATH /venv
ENV PATH="${VENV_PATH}/bin:$PATH"

# Create a virtual environment and install dependencies
RUN python3 -m venv ${VENV_PATH}

# Upgrade pip to the latest version
RUN ${VENV_PATH}/bin/pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Install the dependencies
RUN ${VENV_PATH}/bin/pip install --no-cache-dir -r /requirements.txt

# Create the application directory
RUN mkdir -p ${APP_ROOT}
WORKDIR ${APP_ROOT}

# Copy the application code into the container
COPY . ${APP_ROOT}

# Run collectstatic to gather static files
RUN python manage.py collectstatic --noinput

# Expose the port that uWSGI will listen on
EXPOSE 8000

# Start uWSGI
CMD ["uwsgi", "--ini", "/code/uwsgi.ini"]
