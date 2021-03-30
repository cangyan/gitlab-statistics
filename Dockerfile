FROM python:3.8.8-alpine3.12

WORKDIR /usr/src/app

RUN  mkdir -p /output
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]