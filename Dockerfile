FROM python:3.8-alpine

WORKDIR /

COPY . .

RUN python -m pip install --upgrade pip

RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev 

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py" ]

