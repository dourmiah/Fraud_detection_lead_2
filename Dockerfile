FROM continuumio/miniconda3
WORKDIR /home/app
COPY . . 
RUN apt upgrade -y 
RUN pip install -r requirements.txt 
ENV PYTHONPATH=/home/app
CMD ["pytest", "/home/app/Model/tests/tests.py"]