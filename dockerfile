FROM python:3.11-alpine

WORKDIR /state

COPY . /state

RUN ls -al

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
