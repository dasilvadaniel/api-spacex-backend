import sys
import json
import logging
import boto3
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_config(secret_name):

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name="us-east-2"
    )

    return json.loads(client.get_secret_value(SecretId=secret_name)["SecretString"])


def lambda_handler(event, context):
    """
    This function fetches content from Postgres RDS instance
    """

    try:

        date = event.get("date")
        satellite_id = event.get("satellite_id")

        secret = get_config("starlink-credentials")
        full_result = secret["rds_full_result"]

        conn = psycopg2.connect(database=secret["rds_database"],
                                user=secret["rds_user"],
                                password=secret["rds_password"],
                                host=secret["rds_endpoint"],
                                port=secret["rds_port"])

        logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")

        with conn.cursor() as cur:
            cur.execute(f"""
                        select 
                             longitude, latitude
                        from {full_result}
                        where
                            id = '{satellite_id}' 
                            and cast(creation_date as date) = '{date}'
    
                        order by creation_date DESC
                        limit 1
            """)

            result = cur.fetchone()

            if result:
                result = {"id": satellite_id, "longitude": result[0], "latitude": result[1]}
                logger.info("SUCCESS: Query satellite position succeeded")

            else:
                result = {"id": satellite_id, "longitude": None, "latitude": None}
                logger.info("WARNING: Query satellite position succeeded")

            return result

    except Exception as e:

        logger.error("ERROR: Unexpected error: Could not finish the pipeline.")
        logger.error(e)
        sys.exit()





