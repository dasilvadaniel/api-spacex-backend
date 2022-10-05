import awswrangler as wr
import pandas as pd
import boto3
import json
import sys
from sqlalchemy import create_engine


def get_config(secret_name, secret_value):

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name="us-east-2"
    )

    result = json.loads(client.get_secret_value(SecretId=secret_name)['SecretString'])

    return result[secret_value]


def main(args):

    try:

        secret_name = f"{args[1]}-credentials"
        user = get_config(secret_name, "rds_user")
        password = get_config(secret_name, "rds_password")
        endpoint = get_config(secret_name, "rds_endpoint")
        port = get_config(secret_name, "rds_port")
        database = get_config(secret_name, "rds_database")
        s3_raw_data = get_config(secret_name, "s3_raw_data")
        full_result = get_config(secret_name, "rds_full_result")

        df = wr.s3.read_json(path=s3_raw_data)
        df = df.join(df['spaceTrack'].apply(pd.Series)).drop('spaceTrack', axis=1)

        conn_string = f"postgresql://{user}:{password}@{endpoint}:{port}/{database}"
        engine = create_engine(conn_string)
        conn = engine.connect()

        df.to_sql(full_result, con=conn, if_exists="replace", index=False)

    except Exception as e:

        raise e


if __name__ == "__main__":
    main(sys.argv)




