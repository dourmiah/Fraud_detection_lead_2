import glob
import json
import os
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import (BranchPythonOperator,
                                               PythonOperator)
from airflow.sensors.python import PythonSensor
from airflow.operators.email_operator import EmailOperator

from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from evidently.pipeline.column_mapping import ColumnMapping

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 1),
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}

DATA_DIR = "/opt/airflow/data"


def _load_files(data_logs_filename):
    """Returns reference sample DataFrame, the data logs DataFrame and a
    ColumnMapping object, with numerical and categorial features set.
    """
    reference = pd.read_csv(f"{DATA_DIR}/reference/fraudTest-sample.csv")
    reference = reference.select_dtypes(include="number") # We keep only numbers

    data_logs = pd.read_csv(data_logs_filename)
    data_logs = data_logs.select_dtypes(include="number")

    return reference, data_logs


def _detect_file(**context):
    """Detects if a file named `*.csv` is inside `./data/data-drift` folder.

    If yes, it saves the full path to XCom and return True. False otherwise.
    """
    data_logs_list = glob.glob(f"{DATA_DIR}/data-drift/*.csv")
    if not data_logs_list:
        return False
    data_logs_filename = max(data_logs_list, key=os.path.getctime)
    context["task_instance"].xcom_push(key="data_logs_filename", value=data_logs_filename)
    return True


def _detect_data_drift(**context):
    """Load the CSV and run the data-drift detections.
    """
    data_logs_filename = context["task_instance"].xcom_pull(key="data_logs_filename")
    reference, data_logs = _load_files(data_logs_filename)

    data_drift_report = Report(metrics=[
        DataDriftPreset(stattest_threshold=0.1),
    ])

    data_drift_report.run(current_data=data_logs, reference_data=reference, column_mapping=None)

    report = data_drift_report.as_dict()

    if report["metrics"][0]["result"]["dataset_drift"]:
        return "data_drift_detected"
    else:
        return "no_data_drift_detected"


def _data_drift_detected(**context):
    """Produces a HTML report.
    """
    data_logs_filename = context["task_instance"].xcom_pull(key="data_logs_filename")
    reference, data_logs = _load_files(data_logs_filename)

    data_drift_report = Report(metrics=[
        DataDriftPreset(),
    ])

    data_drift_report.run(current_data=data_logs, reference_data=reference, column_mapping=None)
    data_drift_report.save(f"{DATA_DIR}/data_drift_dashboard_report.html")

def _clean_file(**context):
    data_logs_filename = context["task_instance"].xcom_pull(key="data_logs_filename")
    os.remove(data_logs_filename)


with DAG(dag_id="drift_detection_dag", default_args=default_args, schedule_interval="0 16 * * *", catchup=False) as dag:
    
    # Detect a new file in the directory
    detect_file = PythonSensor(
        task_id="detect_file",
        python_callable=_detect_file,
        poke_interval=20,
        timeout=60,
        mode="poke",
    )

    # Check if a drift exists in data
    detect_data_drift = BranchPythonOperator(
        task_id="detect_data_drift",
        python_callable=_detect_data_drift,
    )

    # Drift detected
    data_drift_detected = PythonOperator(
        task_id="data_drift_detected",
        python_callable=_data_drift_detected,
    )

    # Send an email
    send_email = EmailOperator(
        task_id="send_email",
        to="jedhaprojetfrauddetect2@gmail.com",
        subject="Data Drift Detected",
        html_content="<p>Data drift has been detected. Please review the report attached.</p>",
    )

    # No drift detected
    no_data_drift_detected = DummyOperator(task_id="no_data_drift_detected")

    # Clean drift file
    clean_file = PythonOperator(
        task_id="clean_file",
        python_callable=_clean_file,
        trigger_rule="one_success",  # Exécute cette tâche si au moins une tâche précédente réussit
    )

    # End of pipeline
    end = DummyOperator(task_id="end")

    # Configuration des dépendances
    detect_file >> detect_data_drift
    detect_data_drift >> data_drift_detected >> send_email >> clean_file >> end
    detect_data_drift >> no_data_drift_detected >> clean_file >> end
