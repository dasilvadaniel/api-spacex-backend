import awswrangler as wr
import pandas as pd
import logging
import boto3
import json
import sys
from sqlalchemy import create_engine

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_config(secret_name):

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name="us-east-2"
    )

    return json.loads(client.get_secret_value(SecretId=secret_name)["SecretString"])


def main(args):

    try:

        secret = get_config(f"{args[2]}-credentials")
        user = secret["rds_user"]
        password = secret["rds_password"]
        endpoint = secret["rds_endpoint"]
        port = secret["rds_port"]
        database = secret["rds_database"]
        full_result = secret["rds_full_result"]

        df = wr.s3.read_json(path=secret["s3_raw_data"])
        df = df.join(df['spaceTrack'].apply(pd.Series)).drop('spaceTrack', axis=1)
        df.columns = [x.lower() for x in df.columns]
        df['creation_date'] = df['creation_date'].astype('datetime64[ns]')

        conn_string = f"postgresql://{user}:{password}@{endpoint}:{port}/{database}"
        engine = create_engine(conn_string)
        conn = engine.connect()

        logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")

        df.to_sql(full_result, con=conn, if_exists="replace", index=False)

    except Exception as e:

        logger.error("ERROR: Unexpected error: Could not finish the pipeline.")
        logger.error(e)
        sys.exit()


if __name__ == "__main__":
    main(sys.argv)




