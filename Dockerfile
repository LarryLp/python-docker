FROM python:3

WORKDIR /app
COPY main.py .

CMD [ "python", "./main.py", "ALL"]
