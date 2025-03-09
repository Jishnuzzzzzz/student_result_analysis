import sqlite3
import pandas as pd

def create_database_from_csv(df, db_name):
    """
    Creates a SQLite database and inserts data from a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        db_name (str): Name of the database file.
    """
    try:
        # Create database schema
        create_database_schema(df, db_name)

        # Insert data into the database
        insert_data_into_db(df, db_name)

    except Exception as e:
        print(f"Error creating database: {e}")

def create_database_schema(df, db_name):
    """
    Creates a SQLite database with a schema based on the DataFrame's columns and data types.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        db_name (str): Name of the database file.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Generate SQL schema based on DataFrame columns and data types
        columns_with_types = []
        for col in df.columns:
            dtype = df[col].dtype
            if dtype == "int64":
                sql_type = "INTEGER"
            elif dtype == "float64":
                sql_type = "REAL"
            else:
                sql_type = "TEXT"  # Default to TEXT for strings and other types
            columns_with_types.append(f'"{col}" {sql_type}')  # Preserve column names with spaces

        # Create table with dynamic schema
        schema = ", ".join(columns_with_types)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS data ({schema})")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating database schema: {e}")

def insert_data_into_db(df, db_name):
    """
    Inserts data from a DataFrame into the SQLite database.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        db_name (str): Name of the database file.
    """
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql("data", conn, if_exists="replace", index=False)
        conn.close()
    except Exception as e:
        print(f"Error inserting data into database: {e}")