FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

ENV TZ=Etc/GMT+3
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /requirements.txt

RUN apt-get update
RUN apt-get install libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /workspace

WORKDIR TTS/
RUN pip install -U pip setuptools wheel
COPY requirements.txt /requirements2.txt
RUN pip install -r /requirements2.txt
# RUN pip install -e .
WORKDIR ../