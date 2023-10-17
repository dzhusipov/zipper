FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

# RUN apt-get install pkg-config libhdf5-dev
# for proxies 
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000

CMD [ "python", "./main.py" ]
