FROM python:3.7

WORKDIR /app
COPY main.py .

#RUN pip install -r /code/requirements.txt -i https://pypi.douban.com/simple
