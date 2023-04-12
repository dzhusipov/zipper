FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

# for proxies 
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt
COPY . .
EXPOSE 5000

CMD [ "python", "./main.py" ]