import awswrangler as wr
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

df = wr.s3.read_json(path='s3://api-spacex-backend/').head(5)
df = df.join(df['spaceTrack'].apply(pd.Series)).drop('spaceTrack', axis=1)

conn_string = ''
engine = create_engine(conn_string)
conn = engine.connect()

df.to_sql('starlink_historical_data', con=conn, if_exists='replace', index=False)

conn = psycopg2.connect(conn_string)

