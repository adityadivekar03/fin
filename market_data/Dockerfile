FROM python:3.7-slim
RUN apt-get update && apt-get install -y gcc curl wget
RUN apt-get install -y npm && npm install nodemon --global
WORKDIR /market-data-service
COPY ./market_data/requirements.txt requirements.txt
ENV PYTHONPATH /market-data-service
RUN pip install -r requirements.txt
COPY ./market_data/ /market-data-service
EXPOSE 80
#CMD ["python", "main.py"]
