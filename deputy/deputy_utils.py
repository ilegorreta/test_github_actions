import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.dialects import registry
from sqlalchemy import table, Column, String, DateTime


def create_snowflake_engine(
    SNOWSQL_USER,
    SNOWSQL_PWD,
    SNOWSQL_ACCOUNT,
    SNOWSQL_DEST_DB,
    SNOWSQL_DEST_SCHEMA,
    SNOWSQL_WAREHOUSE,
):
    """Create the DB engine and connect to Snowflake."""
    engine = None
    connection = None
    try:
        url = f"snowflake://{SNOWSQL_USER}:{SNOWSQL_PWD}@{SNOWSQL_ACCOUNT}/{SNOWSQL_DEST_DB}/{SNOWSQL_DEST_SCHEMA}?warehouse={SNOWSQL_WAREHOUSE}"
        registry.register("snowflake", "snowflake.sqlalchemy", "dialect")
        engine = create_engine(url)
        connection = engine.connect()
    except Exception as e:
        print("Can't create Snowflake engine")
        print(e)
    return engine, connection


def close_snowflake_connection(engine, connection):
    """Close Snowflake connection."""
    if (connection is not None) and (connection is not None):
        if not connection.closed:
            connection.close()
    if engine is not None:
        engine.dispose()


def get_timesheets_raw_table(table_name, schema_name):
    """Create a SQLalchemy table construct for the TIMESHEETS_RAW table."""
    return table(
        table_name,
        Column("VALUE", String),
        Column("UPLOADED_AT", DateTime),
        schema=schema_name,
    )


def upload_to_snowflake(conn, records, SNOWSQL_DEST_TABLE, SNOWSQL_DEST_SCHEMA):
    """Upload data to Snowflake."""
    try:
        dest_table = get_timesheets_raw_table(SNOWSQL_DEST_TABLE, SNOWSQL_DEST_SCHEMA)
        result = conn.execute(dest_table.insert(), records)
        print(
            f"Uploaded {len(len(result.inserted_primary_key_rows))} records to Snowflake"
        )
    except Exception as e:
        # print("Can't upload data into Snowflake")
        print(e)


def fetch_deputy_records(API_AUTH, TEST_URL):
    """Fetch data from Deputy's Timesheets Endpoint"""
    try:
        search_key = "Date"
        sort_key = "Id"
        join_objects = ["EmployeeObject", "OperationalUnitObject", "RosterObject"]
        get_from_position = 0
        total_records = []
        while True:
            payload = {
                "search": {
                    "f2": {
                        "field": search_key,
                        "type": "ge",
                        "data": "2022-08-27T00:00:00-06:00",
                    },
                    "f1": {
                        "field": search_key,
                        "type": "lt",
                        "data": "2022-08-28T00:00:00-06:00",
                    },
                },
                "sort": {sort_key: "asc"},
                "join": join_objects,
                "start": get_from_position,
            }
            payload2 = json.dumps(payload).encode("utf-8")
            headers = {"Authorization": API_AUTH}
            response = requests.request(
                "POST", TEST_URL, headers=headers, data=payload2
            )
            records = json.loads(response.text)
            total_records.extend(records)
            if len(records) < 500:
                break
            get_from_position += 500
        return total_records
    except Exception as e:
        print(e)
        return None
