FROM python:3.8

WORKDIR /GreenPayBackend

COPY . /GreenPayBackend

COPY ./requirements.txt /GreenPayBackend/requirements.txt

ENV PYTHONPATH /GreenPayBackend
# same as  `export PYTHONPATH=$PYTHONPATH:/home/ubuntu/GreenPayBackend`

RUN pip3 install -r /GreenPayBackend/requirements.txt

CMD ["python", "/GreenPayBackend/src/api/app.py", "|", "tee", "-a" , "./flask-out.txt"]

