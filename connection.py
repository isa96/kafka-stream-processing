#!/usr/bin/python3

import os
import json
from sqlalchemy import create_engine

def warehouse():
    path = open(os.getcwd()+'/config.json')
    conf = json.load(path)['warehouse']
    engine = create_engine(f"postgresql+psycopg2://{conf['user']}:{conf['password']}@{conf['host']}/{conf['database']}")
    return engine