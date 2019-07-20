FROM python:3

RUN mkdir /market-data-service
WORKDIR /market-data-service

ENV PYTHONPATH /market-data-service

COPY . /market-data-service

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

#RUN ["python", "main.py"]