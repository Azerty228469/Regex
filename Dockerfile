FROM debian:11
WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential python3 python3-pip

COPY app.py .
COPY templates /app/templates

RUN pip3 install Flask
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
