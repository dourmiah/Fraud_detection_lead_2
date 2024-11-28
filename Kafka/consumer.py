# Example written based on the official
# Confluent Kakfa Get started guide https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/consumer.py

from confluent_kafka import Consumer, Producer
import json
import ccloud_lib
import time
import mlflow
import sklearn
import pandas as pd
from datetime import datetime, timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import create_engine
import os

# Configuration de la connexion à PostgreSQL
engine = create_engine(os.environ["BDD_URI"])
table_name = 'prediction'

# Requête SQL pour lire les données de la table
query = 'SELECT * FROM prediction'

# Lire les données dans un DataFrame
# df_postgres = pd.read_sql(query, engine)

# print("************************************************************")
# print("df_postgres : ", df_postgres)
# print("df.head : ", df_postgres.head())



# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC_TRANS = "topic_trans"
TOPIC_PREDICT = "topic_predict"

# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer = Producer(producer_conf)

# URL MLFlow
k_MLflow_Tracking_URL = "https://dom-fraud-detection-48e81565c75c.herokuapp.com/"
k_Logged_Model = "runs:/d8db0260a09d4f6e9a16413fb7e4ae77/model"
mlflow.set_tracking_uri(k_MLflow_Tracking_URL)
loaded_model = mlflow.sklearn.load_model(k_Logged_Model)

# Create Consumer instance
# 'auto.offset.reset=earliest' to start reading from the beginning of the
# topic if no committed offsets exist
consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
consumer_conf['group.id'] = 'trans_consumer'
consumer_conf['auto.offset.reset'] = 'earliest' # This means that you will consume latest messages that your script haven't consumed yet!
consumer = Consumer(consumer_conf)

# Subscribe to transaction topic
consumer.subscribe([TOPIC_TRANS])

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

# Sending notification e-mail when found fraud  transaction
def send_email(subject, body, to_email):
    # Informations de connexion
    from_email = os.getenv("FROM_EMAIL")
    from_password = os.getenv("FROM_PASSWORD")
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP et envoi de l'email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Démarrer le chiffrement TLS
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print('Email envoyé avec succès')
    except Exception as e:
        print(f'Échec de l\'envoi de l\'email: {e}')

# Process messages
try:
    while True:
        msg = consumer.poll(1.0) # Search for all non-consumed events. It times out after 1 second
        if msg is None:
            # No message available within timeout.
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            # Check for Kafka message
            record_key = msg.key()
            record_value = msg.value()
            print("**********************************************************************")
            print("record_value", record_value)
            data = json.loads(record_value)
   
            columns = data['data']["columns"]
            index = data['data']["index"]
            rows = data['data']["data"]

            # Convertir le dictionnaire en DataFrame
            df = pd.DataFrame(rows, columns=columns)

            # ! DANGER - 17 is hard coded
            col = df["current_time"]
            df.insert(17, "unix_time", col)

            # convert to date string
            df.rename(columns={"current_time": "trans_date_trans_time"}, inplace=True)

            
            print("df : ", df)
            
            timestamp = df["trans_date_trans_time"].iloc[0]

            date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
            str_date = date.strftime("%Y-%m-%d %H:%M:%S")
            
            df["trans_date_trans_time"] = df["trans_date_trans_time"].astype(str)
            df.at[index[0], "trans_date_trans_time"] = str_date

            
            df["trans_date_trans_time"] = str_date
            print('df["trans_date_trans_time"]', df["trans_date_trans_time"])

            # reorder columns
            cols = df.columns.tolist()
            reordered_cols = [cols[-1]] + cols[:-1]
            df = df[reordered_cols]

            # Ne garde que les colonnes attendues pour faire tourner le modèle (vire aussi la colonne is_fraud)
            model_columns = loaded_model.feature_names_in_ if hasattr(loaded_model, "feature_names_in_") else []
            prediction = loaded_model.predict(df[model_columns])
            print("Prediction : ", prediction)
            
            # Add new column 'prediction'
            df['prediction'] = prediction
            
            # Send a mail if a fraud is detected => REtrouver les credentials mail
            # if prediction[0] == 1:
            #     print("Fraud détectée !")
            #     send_email(
            #     subject='Fraud detection',
            #     body='A fraudulent transaction has been detected !',
            #     to_email='jedhaprojetfrauddetect@gmail.com'
            #     )
           
            # Write data to TOPIC_PREDICT
            record_key = "prediction"
            print("df (2): ", df)
            record_value = df.to_json()
            
            print("record_value (2) : ", record_value)

            producer.produce(
            TOPIC_PREDICT,
            key=record_key,
            value=record_value,
            on_delivery=acked
            )

            # Write data to database
            df.to_sql(table_name, engine, if_exists='append', index=False)

            # !!!!!!!!!!!   NE PAS AJOUTER DANS Le CODE !!!!!!!!!!!!!
            # insert into prediction 
            # (trans_date_trans_time,cc_num,merchant,category,amt,first,last,gender,street,city,state,zip,lat,long,city_pop,job,dob,trans_num,unix_time,merch_lat,merch_long,is_fraud,prediction)
            # values('2020-10-13 09:53:40','501899453424','fraud_Langosh, Wintheiser and Hyatt','food_dining',164.05,'Jessica','Dominguez','F','06393','Nancy Parkways Suite 855','Gadsden AL','35903',33.9845,-85.9077,'67082','Ceramics designer','1970-01-08','e83caea210536d9d85e7415207f962d4',1381658020,33.819701,-85.461329,'0','Not Fraud')

except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()