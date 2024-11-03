import os
import json
import time
import ccloud_lib
import pandas as pd
from typing import Optional
from sqlalchemy import create_engine, types
from confluent_kafka import Consumer, KafkaException


k_Topic_2 = "topic_2"
k_GroupId = "python-group-1"
k_Client_Prop = "client.properties"

k_table_name = "fraud_detection_2_table"


# -----------------------------------------------------------------------------
def read_transaction_from_topic_2(consumer: Consumer) -> Optional[pd.DataFrame]:  # Union[pd.DataFrame, None]
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                raise KafkaException(msg.error())

            json_str = msg.value().decode("utf-8")
            print(f"Received msg : {json_str}\n\n", flush=True)

            try:
                # json_dict = json.loads(json_str)
                # print("json_dict : ", json_dict)
                # return None
                data_list = json.loads(json_str)  # JSON vers liste de dictionnaires
                df = pd.DataFrame(data_list)  # Liste de dicts vers DataFrame
                # print(df)
                # df = pd.DataFrame(data=json_dict["data"], columns=json_dict["columns"], index=json_dict["index"])
                return df
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error in JSON format : {e}", flush=True)
                continue

    except KeyboardInterrupt:
        print("CTRL+C detected. Closing gently.", flush=True)

    finally:
        consumer.close()

    return None


# -----------------------------------------------------------------------------
def create_topic_consumer() -> Consumer:

    conf = ccloud_lib.read_ccloud_config(k_Client_Prop)

    # defines the ID of the consumer group to which the consumer belongs
    conf["group.id"] = k_GroupId

    # the consumer starts reading at the beginning if no offset has been recorded for him or continue to read from where he left off.
    # ! The offset for each partition is stored at group level, NOT at individual consumer level.
    # So a consumer joining the same group will pick up where the last one left off
    # If you change the group name (python-group-42), the user will read the earliest message.
    conf["auto.offset.reset"] = "earliest"

    consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    consumer = Consumer(consumer_conf)
    consumer.subscribe([k_Topic_2])
    return consumer


# -----------------------------------------------------------------------------
if __name__ == "__main__":

    print("Logger SQL started", flush=True)

    consumer = create_topic_consumer()

    try:
        current_transaction = read_transaction_from_topic_2(consumer)
        print(current_transaction, flush=True)
    except KafkaException as e:
        print(f"Kafka error : {e}", flush=True)

    database_url = os.getenv("LOGGER_SQL_URI")
    engine = create_engine(database_url)

    print("Logger SQL will be done in 5 sec", flush=True)
    time.sleep(5)


# # -----------------------------------------------------------------------------
# def get_sqlalchemy_type(dtype):
#     if pd.api.types.is_integer_dtype(dtype):
#         return types.Integer
#     elif pd.api.types.is_float_dtype(dtype):
#         return types.Float
#     elif pd.api.types.is_string_dtype(dtype):
#         return types.String
#     elif pd.api.types.is_datetime64_any_dtype(dtype):
#         return types.DateTime
#     else:
#         raise ValueError(f"Type non supporté : {dtype}")


# # -----------------------------------------------------------------------------
# def create_table_from_dataframe(df, table_name):
#     column_types = {col: get_sqlalchemy_type(dtype) for col, dtype in df.dtypes.items()}

#     with engine.begin() as conn:
#         df.head(0).to_sql(table_name, conn, if_exists="replace", index=False, dtype=column_types)

#     print(f"Table '{table_name}' créée avec succès.", flush=True)


# # -----------------------------------------------------------------------------
# def insert_observation(df_observation, table_name):
#     if len(df_observation) != 1:
#         raise ValueError("df_observation doit contenir une seule ligne.")

#     with engine.begin() as conn:
#         df_observation.to_sql(table_name, conn, if_exists="append", index=False)

#     print("Observation insérée avec succès.", flush=True)


# # -----------------------------------------------------------------------------
# def insert_dataframe(df, table_name):

#     with engine.begin() as conn:
#         df.to_sql(table_name, conn, if_exists="append", index=False)
#     print(f"Le DataFrame a été inséré avec succès dans la table '{table_name}'.", flush=True)


# # -----------------------------------------------------------------------------
# def fetch_table_content(table_name):
#     with engine.connect() as conn:
#         query = f"SELECT * FROM {table_name};"
#         df = pd.read_sql(query, conn)
#     print(df, flush=True)
#     return df
