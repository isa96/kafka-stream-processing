#!/usr/bin/python3

import os
import json
import pickle
import pandas as pd
import connection
from kafka import KafkaConsumer
from category_encoders import OrdinalEncoder

import warnings
warnings.filterwarnings('ignore')

def transform(df):
    df = df.drop(['Id', 'logTimestamp'], axis=1)
    df.columns = ['device', 'activity']
    encoder = OrdinalEncoder()
    df = encoder.fit_transform(df)
    return df

if __name__ == '__main__':

    consumer = KafkaConsumer('aaa', bootstrap_servers='localhost')

    for message in consumer:

        data = json.loads(message.value)
        df = pd.DataFrame([data])
        df.to_sql('user_activity', connection.warehouse(), if_exists='append', index=False)
        print(f'Records = {data}')

        model = pickle.load(open(os.getcwd()+'/model/model.pkl', 'rb'))
        prediction = 'Not Fraud' if model.predict(transform(df)) == 0 else 'Fraud'

        df = pd.DataFrame([{'Id': data['Id'], 'userFlag':prediction}])
        df.to_sql('user_fraud', connection.warehouse(), if_exists='append', index=False)
        print(f'Prediction: {prediction}')
