from psycopg2 import connect, DatabaseError
from typing import Union


def execute_sql(command: str):
    """ Execute sql command and return result"""

    db = 'host=db dbname=postgres user=postgres password=postgres'

    try:
        with connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                try:
                    response = cur.fetchall()
                except DatabaseError:  # In case it does't return anything
                    return ''

    except DatabaseError as error:
        raise Exception(error)

    if conn is not None:
        conn.close()
    return response


def create_table(table_name: str, fields: dict[str: Union[str, int, float, bool, dict]]):
    """Create new table"""

    if is_table(table_name):
        raise Exception('Table already exists')

    command = f"""
    CREATE TABLE "{table_name}" (
        """

    for name, variable_type in fields.items():
        command += f'{name} {variable_type}, '
    command = command[:-2] + ');'

    execute_sql(command)


def add_row(table_name: str, row: dict[str: Union[str, int, float, bool, dict], ]):
    """Add new row"""

    if not is_table(table_name):
        raise Exception("Table doesn't exist")

    command = f"""
        INSERT INTO "{table_name}" (
        """

    for field in row.keys():
        command += f'{field}, '
    command = command[:-2] + ') VALUES ('

    for value in row.values():
        if type(value) is str:
            command += f"'{value}', "
        else:
            command += f"{value}, "
    command = command[:-2] + ');'

    execute_sql(command)


def update_row(table_name: str,
               old_value: dict[str: Union[str, int, float, bool, dict]],
               new_value: dict[str: Union[str, int, float, bool, dict]]):
    """Change value in table"""

    command = f"""UPDATE "{table_name}"
                SET {list(old_value.keys())[0]} = {list(new_value.values())[0]}
                WHERE {list(new_value.keys())[0]} = {list(old_value.values())[0]}
                ;"""

    execute_sql(command)


def delete_row(table_name: str, field_name: str, field_value: Union[str, int, float, bool, dict]):
    """Delete row from table"""

    command = f"""DELETE FROM "{table_name}"
                    WHERE {field_name} = {field_value}
                    ;"""

    execute_sql(command)


def get_data(table_name: str, field='*'):
    """Get data from table. Leave field blank to get all rows"""

    if not is_table(table_name):
        return "Table doesn't exist"

    command = f"""
    SELECT {field} FROM "{table_name}"
    ;"""

    return execute_sql(command)


def is_table(table_name: str):
    """Check if table exists"""

    command = f"SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    tables = [x[1] for x in execute_sql(command)]

    if table_name in tables:
        return True
    return False
