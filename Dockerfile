# Our docker-compose file uses Dockerfile-dev instead of Dockerfile
FROM python:3.6

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

COPY scripts/docker_script.sh /docker_script.sh
RUN chmod +x /docker_script.sh

EXPOSE 5000