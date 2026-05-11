import os

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

    connection = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        charset="utf8mb4",
        autocommit=False,
    )

    statements = [
        "DROP DATABASE IF EXISTS bd_api_employees",
        "CREATE DATABASE bd_api_employees CHARACTER SET utf8mb4",
        "USE bd_api_employees",
        """
        CREATE TABLE employees (
            id INT(11) NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            age INT(11) NOT NULL,
            PRIMARY KEY (id)
        )
        """,
        "INSERT INTO employees(name, age) VALUES ('Jake', 21)",
        "INSERT INTO employees(name, age) VALUES ('Mathew', 24)",
        "INSERT INTO employees(name, age) VALUES ('Bob', 35)",
    ]

    try:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    print("Base bd_api_employees creada y cargada con datos de ejemplo")


if __name__ == "__main__":
    main()
