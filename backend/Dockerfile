FROM python:3.9
# ARG port

USER root

WORKDIR meli-challenge/backend

# ENV PORT=$port

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt-get update 
RUN apt-get install -y libmariadb3
RUN pip3 install mariadb


ADD ./backend/requirements.txt ./

RUN chgrp -R 0 /meli-challenge \
    && chmod -R g=u /meli-challenge \
    && pip install pip --upgrade \
    && pip install -r requirements.txt




# EXPOSE $PORT

ADD ./backend/ .
ADD ./common/ .
ADD ConfigFile.properties .

ENV TZ="America/Montevideo"
RUN date

RUN ls -la

# CMD gunicorn app:app --bind 0.0.0.0:$PORT --preload
CMD ["python", "app.py"]