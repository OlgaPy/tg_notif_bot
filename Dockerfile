# first stage
FROM python:3.9-slim as builder
MAINTAINER Olga Pykhova
ADD . /app
WORKDIR /app
# Compile python dependencies as wheels into specialized folder
RUN mkdir /wheels && pip3 install --upgrade pip setuptools wheel && pip3 wheel -r requirements.txt --wheel-dir=/wheels


# second stage
FROM python:3.9-slim
# Transfer already build wheels
COPY --from=builder /wheels /wheels
ADD . /app
WORKDIR /app
RUN pip3 install --no-index --find-links=/wheels -r requirements.txt
VOLUME /db
CMD [ "python3", "bot.py"]
