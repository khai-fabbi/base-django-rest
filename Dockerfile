FROM python:3.9.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    libffi-dev \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev  \
    libssl-dev \
    nano

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

RUN mkdir -p /vol/web
RUN mkdir -p /vol/sock

# EXPOSE 8008

COPY ./scripts /scripts
RUN chmod +x /scripts/entrypoint.sh
RUN chmod +x /scripts/cron.sh

CMD ["/scripts/entrypoint.sh"]