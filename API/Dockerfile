FROM continuumio/miniconda3

WORKDIR /home/app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

RUN apt-get update -y 
RUN apt-get install nano unzip
RUN apt-get install -y python3.10
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD gunicorn app:app  --bind 0.0.0.0:$PORT --worker-class uvicorn.workers.UvicornWorker 