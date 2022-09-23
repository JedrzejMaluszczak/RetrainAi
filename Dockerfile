FROM python:3.8

ENV PYTHONUNBUFFERED=1
WORKDIR /code
ARG requirements_file
ENV REQUIREMENTS_FILE ${requirements_file:-dev-requirements.txt}
ADD /config/requirements/base-requirements.txt /config/requirements/$REQUIREMENTS_FILE /tmp/

RUN pip3 install --no-cache-dir -r /tmp/$REQUIREMENTS_FILE
RUN curl -o /usr/local/bin/waitforit -sSL https://github.com/maxcnunes/waitforit/releases/download/v2.4.1/waitforit-linux_amd64 && chmod +x /usr/local/bin/waitforit
COPY . /code/
