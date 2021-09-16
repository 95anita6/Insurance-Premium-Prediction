from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd
import os

def getDBSession():
    """Create and get a Cassandra session"""
    cloud_config= {
            'secure_connect_bundle': os.environ.get('ASTRA_PATH_TO_SECURE_BUNDLE')
    }
    auth_provider = PlainTextAuthProvider(os.environ.get('ASTRA_CLIENT_ID'), os.environ.get('ASTRA_CLIENT_SECRET'))
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    return session

def retrieveInsertedData(session):
    """A function which retrieves data from Cassandra"""

    select_query = session.prepare("\
                SELECT * FROM insurance_premium.insurance\
                ")
    try:
        df = pd.DataFrame(list(session.execute(select_query)))
        print("Success")
#        print(df)
        df.to_csv('insurance_premium.csv', index=False)
    except Exception as e: 
        print(e)

def main():
    """The main routine."""
    session = getDBSession()
    retrieveInsertedData(session)

if __name__ == "__main__":
    main()