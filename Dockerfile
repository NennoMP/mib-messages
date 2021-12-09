#
# Docker file for Message in a Bottle v1.0
#
FROM python:3.9
LABEL maintainer="5_squad"
LABEL version="1.0"
LABEL description="Message in a Bottle User Microservice"

# creating the environment
COPY . /app
# setting the workdir
WORKDIR /app

# installing all requirements
RUN ["pip", "install", "-r", "requirements.prod.txt"]
ENV CELERY_BROKER_URL=redis://redis:6381/0
ENV CELERY_RESULT_BACKEND=redis://redis:6381/0

# exposing the port
EXPOSE 5002/tcp

# Main command
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]