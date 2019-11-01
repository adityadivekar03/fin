FROM python:3.7-slim
RUN apt-get update && apt-get install -y gcc curl wget
RUN apt-get install -y npm && npm install nodemon --global
WORKDIR /market_data
COPY ./market_data/requirements.txt requirements.txt
ENV PYTHONPATH /market_data
RUN pip install -r requirements.txt
COPY ./market_data/ /market_data
COPY ./common_utils /market_data/common_utils
EXPOSE 80
