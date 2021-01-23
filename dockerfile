FROM python:3.6

# バイナリレイヤ下での標準出力とエラー出力を抑制します。（PYTHONUNBUFFERED
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/