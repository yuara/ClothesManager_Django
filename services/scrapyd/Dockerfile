FROM python:3.8.3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y cron

COPY scrapyd.sh ./
RUN chmod 0755 /usr/src/app/scrapyd.sh

COPY ./scrapyd.conf ./scraping  ./

COPY ./cron-d ./
RUN crontab cron-d

ENTRYPOINT ["/usr/src/app/scrapyd.sh"]
