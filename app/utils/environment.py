import os

from dotenv import load_dotenv


def get_mysql_config() -> dict[str, str | int]:
    load_dotenv()
    required_variables = (
        "MYSQL_HOST",
        "MYSQL_DATABASE",
        "MYSQL_USER",
        "MYSQL_PASSWORD",
    )
    missing_variables = [
        name for name in required_variables if not os.getenv(name)
    ]
    if missing_variables:
        missing = ", ".join(missing_variables)
        raise RuntimeError(
            f"Faltan variables de entorno de MySQL: {missing}."
        )

    port_value = os.getenv("MYSQL_PORT", "3306")
    try:
        port = int(port_value)
    except ValueError as error:
        raise RuntimeError("MYSQL_PORT debe ser un número entero.") from error

    return {
        "host": os.environ["MYSQL_HOST"],
        "port": port,
        "database": os.environ["MYSQL_DATABASE"],
        "user": os.environ["MYSQL_USER"],
        "password": os.environ["MYSQL_PASSWORD"],
    }
