# pull official base image
FROM python:3.8.3-alpine


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install zlib, a required dependency for pillow and postgres
# gcc python3-dev jpeg-dev zlib-dev for pillow
RUN apk update \
 && apk add --virtual build-tools gcc python3-dev musl-dev jpeg-dev zlib-dev \
 && apk add postgresql-dev libjpeg curl


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
COPY ./cron-d .

RUN /usr/bin/crontab cron-d

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
