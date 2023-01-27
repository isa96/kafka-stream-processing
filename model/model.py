#!/usr/bin/python3

import os
import pickle
import pandas as pd
from category_encoders import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('fraud.csv')
X = df.drop(['isFraud', 'timeformat1', 'timeformat2'], axis=1)
X.columns = ['activity', 'device']
y = df['isFraud']

encoder = OrdinalEncoder()
X = encoder.fit_transform(X)

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

pickle.dump(model, open(os.getcwd()+'/model.pkl', 'wb'))