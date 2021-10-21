FROM python:3.7.6


WORKDIR /patent_search_engine_1

COPY ./patent_search_engine ./patent_search_engine

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN ["apt-get", "update"]
RUN ["apt-get", "-y", "install", "vim"]

CMD ["python3", "./patent_search_engine/flaskblog.py"]

