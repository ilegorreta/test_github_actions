import os
import json
from datetime import datetime

from deputy_utils import (
    create_snowflake_engine,
    close_snowflake_connection,
    upload_to_snowflake,
    fetch_deputy_records,
)

TIMESHEETS_ENDPOINT = os.getenv("TIMESHEETS_ENDPOINT")
API_AUTH = os.getenv("DEPUTY_API_KEY")
SNOWSQL_ACCOUNT = os.getenv("SNOWSQL_ACCOUNT")
SNOWSQL_USER = os.getenv("SNOWSQL_USER")
SNOWSQL_PWD = os.getenv("SNOWSQL_PWD")
SNOWSQL_WAREHOUSE = os.getenv("SNOWSQL_WAREHOUSE")
SNOWSQL_DEST_SCHEMA = os.getenv("SNOWSQL_DEST_SCHEMA")
SNOWSQL_DEST_DB = os.getenv("SNOWSQL_DEST_DB")
SNOWSQL_DEST_TABLE = os.getenv("SNOWSQL_DEST_TABLE")


def main():
    records = fetch_deputy_records(API_AUTH, TIMESHEETS_ENDPOINT)
    try:
        if len(records) > 0:
            print("Creating:")
            snow_engine, snow_conn = create_snowflake_engine(
                SNOWSQL_USER,
                SNOWSQL_PWD,
                SNOWSQL_ACCOUNT,
                SNOWSQL_DEST_DB,
                SNOWSQL_DEST_SCHEMA,
                SNOWSQL_WAREHOUSE,
            )
            dt = datetime.now()
            records_to_upload = []
            for deputy_object in records:
                snowflake_record = {
                    "VALUE": json.dumps(deputy_object),
                    "UPLOADED_AT": dt,
                }
                records_to_upload.append(snowflake_record)
            upload_to_snowflake(
               snow_conn, records_to_upload, SNOWSQL_DEST_TABLE, SNOWSQL_DEST_SCHEMA
            )
    except Exception:
        print("Exception uploading records to Snowflake.")
    finally:
        close_snowflake_connection(snow_engine, snow_conn)


if __name__ == "__main__":
    main()
