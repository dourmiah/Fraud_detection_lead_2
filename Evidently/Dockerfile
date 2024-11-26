FROM apache/airflow:2.7.3

COPY requirements.txt .
USER airflow
RUN pip install -r requirements.txt

RUN pip uninstall dataclasses -y
