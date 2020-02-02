FROM python:3

MAINTAINER Zixuan Guo <i@zxguo.me>

# setup directory
COPY . /app
WORKDIR /app

# install dependency for service
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app/MycologyBot.py"]
