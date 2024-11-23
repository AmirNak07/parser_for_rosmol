FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt && \
apk update && \
apk add firefox geckodriver xvfb

COPY . .

CMD [ "python", "-u", "main.py" ]