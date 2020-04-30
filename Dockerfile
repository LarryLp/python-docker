FROM frolvlad/alpine-python3:latest

WORKDIR /app
COPY main.py .
COPY iaas .
COPY validation.py .
#CMD [ "python", "./main.py", "ALL"]
