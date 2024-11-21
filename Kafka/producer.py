# Code inspired from Confluent Cloud official examples library
# https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/producer.py

from confluent_kafka import Producer
import json
import ccloud_lib # Library not installed with pip but imported from ccloud_lib.py
import numpy as np
import time
import requests
import threading

# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC_TRANS = "topic_trans" # Topic des transactions
TOPIC_PREDICT = "topic_predict" # Topic des prédictions

# API transactions url
url = "https://real-time-payments-api.herokuapp.com/current-transactions"

# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer = Producer(producer_conf)

# Create topics if they do not already exist
ccloud_lib.create_topic(CONF, TOPIC_TRANS)
ccloud_lib.create_topic(CONF, TOPIC_PREDICT)


delivered_records = 0

# Callback called acked (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    global delivered_records
    # Delivery report handler called on successful or failed delivery of message
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
                .format(msg.topic(), msg.partition(), msg.offset()))

def task():
    response = requests.get(url)
    data = response.json()

    if isinstance(data, str):
        data = json.loads(data) # Parse a JSON to a Python dictionary
   
    record_key = "transaction"
    record_value = json.dumps(
        {
            "data": data
        }
    )
    # Send data to transactions Topic
    producer.produce(
            TOPIC_TRANS,
            key=record_key,
            value=record_value,
            on_delivery=acked
        )

    producer.poll(0)


def periodic_task(interval, func):
    try:
        while True:
            func()
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush() # Finish producing the latest event before stopping the whole script

t = threading.Thread(target=periodic_task, args=(20, task))
t.start()