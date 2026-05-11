import csv
import os
import re

import boto3
import pymysql


def get_env(name, default=None, required=False):
    value = os.environ.get(name, default)
    if required and not value:
        raise ValueError(f"Falta la variable de entorno {name}")
    return value


def main():
    mysql_host = get_env("MYSQL_HOST", "3.90.112.210")
    mysql_port = int(get_env("MYSQL_PORT", "8005"))
    mysql_user = get_env("MYSQL_USER", required=True)
    mysql_password = get_env("MYSQL_PASSWORD", required=True)
    mysql_database = get_env("MYSQL_DATABASE", required=True)
    mysql_table = get_env("MYSQL_TABLE", required=True)
    csv_file = get_env("CSV_FILE", "data.csv")
    s3_bucket = get_env("S3_BUCKET", "gcr-output-01")
    s3_key = get_env("S3_KEY", os.path.basename(csv_file))

    if not re.fullmatch(r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)?", mysql_table):
        raise ValueError("MYSQL_TABLE solo puede contener letras, números, '_' y un punto opcional para schema.table")

    connection = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.Cursor,
        connect_timeout=10,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{mysql_table.replace('.', '`.`')}`")
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description or []]

        with open(csv_file, "w", newline="", encoding="utf-8") as csv_handle:
            writer = csv.writer(csv_handle)
            if headers:
                writer.writerow(headers)
            writer.writerows(rows)
    finally:
        connection.close()

    s3 = boto3.client("s3")
    s3.upload_file(csv_file, s3_bucket, s3_key)

    print(f"CSV generado en {csv_file}")
    print(f"CSV subido a s3://{s3_bucket}/{s3_key}")
    print("Ingesta completada")


if __name__ == "__main__":
    main()
