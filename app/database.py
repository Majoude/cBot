# Importing necessary libraries

import sqlite3
from config import settings
import os

data_name = os.environ.get("BOT_DATA")

# Creating a new class that includes the database functions

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect(settings.data_name)

    @staticmethod
    def insert_record(table_name, column_value_dict):
        """
    Inserts a record into the specified table in the SQLite database.

    Args:
        table_name (str): The name of the table where the record will be inserted.
        column_value_dict (dict): A dictionary where keys are column names and values are the data to be inserted.

    Returns:
        int: The ID of the inserted record if successful, None otherwise.
    
    Raises:
        sqlite3.Error: If there is an error during the database operation.
    """
        try:
            # Connect to the SQLite3 database
            conn = Database.connect()
            
            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()
            
            # Construct the SQL query to insert a record
            columns = ', '.join(column_value_dict.keys())
            placeholders = ', '.join(['?' for _ in column_value_dict])
            sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Extract values to be inserted
            values = tuple(column_value_dict.values())

            # Execute the SQL query to insert the record
            cursor.execute(sql_query, values)

            # Get the ID of the last inserted row
            record_id = cursor.lastrowid

            # Commit changes and close connection
            conn.commit()
            conn.close()
            return record_id
        except sqlite3.Error as e:
            print(f"Error inserting record: {e}")
            return None

    @staticmethod
    def update_table_values(table_name, column_value_dict, condition):
        """
    Updates values in the specified table based on the given condition.

    Args:
        table_name (str): The name of the table where the values will be updated.
        column_value_dict (dict): A dictionary where keys are column names and values are the new data.
        condition (str): The condition for updating the records (e.g., "id = 1").

    Raises:
        sqlite3.Error: If there is an error during the database operation.
    """
        try:
            # Connect to the SQLite3 database
            conn = sqlite3.connect(data_name)

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Construct the SET part of the SQL query
            set_query = ', '.join([f"{column} = ?" for column in column_value_dict.keys()])

            # Construct the SQL query
            sql_query = f"UPDATE {table_name} SET {set_query} WHERE {condition}"

            # Extract values to be updated
            values = tuple(column_value_dict.values())

            # Execute the SQL query
            cursor.execute(sql_query, values)

            # Commit changes and close connection
            conn.commit()
            conn.close()

            print(f"Values updated successfully in the table '{table_name}'.")
    
        except sqlite3.Error as e:
            print(f"Error updating values in the table '{table_name}': {e}")


    @staticmethod
    def delete_all_data_from_table(table_name):
        """
    Deletes all data from the specified table in the SQLite database.

    Args:
        table_name (str): The name of the table from which data will be deleted.

    Raises:
        sqlite3.Error: If there is an error during the database operation.
    """
        try:
            # Connect to the SQLite3 database
            conn = sqlite3.connect(data_name)

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Delete all data from the specified table
            cursor.execute(f'DELETE FROM {table_name}')

            # Commit changes and close connection
            conn.commit()
            conn.close()

            print(f"All data deleted from the table '{table_name}' successfully.")
    
        except sqlite3.Error as e:
            print(f"Error deleting data from the table '{table_name}': {e}")
    
    
    @staticmethod
    def delete_table(table_name):
        """
    Deletes the specified table from the SQLite database.

    Args:
        table_name (str): The name of the table to be deleted.

    Raises:
        sqlite3.Error: If there is an error during the database operation.
    """
        try:
            # Connect to the SQLite3 database
            conn = sqlite3.connect(data_name)

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Construct the SQL query to drop the table
            sql_query = f"DROP TABLE IF EXISTS {table_name}"

            # Execute the SQL query to drop the table
            cursor.execute(sql_query)

            # Commit changes and close connection
            conn.commit()
            conn.close()

            print(f"Table '{table_name}' deleted successfully.")
        
        except sqlite3.Error as e:
            print(f"Error deleting table '{table_name}': {e}")


    @staticmethod
    def retrieve_records_as_dicts(table_name, **conditions):
        """
    Retrieves records from the specified table as a list of dictionaries.

    Args:
        table_name (str): The name of the table from which records will be retrieved.
        **conditions: Optional conditions for filtering the records (e.g., column_name=value).

    Returns:
        list: A list of dictionaries, where each dictionary represents a record with column names as keys.

    Raises:
        sqlite3.Error: If there is an error during the database operation.
    """
        try:
            # Connect to SQLite3 database
            conn = sqlite3.connect(data_name)
            cursor = conn.cursor()

            # Define the base query
            query = f"SELECT * FROM {table_name}"

            # If conditions are provided, construct WHERE clause
            if conditions:
                query += " WHERE "
                conditions_list = []
                values = []

                # Construct the conditions
                for key, value in conditions.items():
                    conditions_list.append(f"{key} = ?")
                    values.append(value)

                # Join the conditions using AND
                query += " AND ".join(conditions_list)

                # Execute the query with provided conditions
                cursor.execute(query, values)
            else:
                # Execute the query without any conditions
                cursor.execute(query)

            # Fetch all records
            records = cursor.fetchall()

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]

            # Close connection
            conn.close()

            # Create a list of dictionaries where each dictionary represents a record
            records_as_dicts = []
            for record in records:
                record_dict = {}
                for i, column in enumerate(columns):
                    record_dict[column] = record[i]
                records_as_dicts.append(record_dict)

                return records_as_dicts
    
        except sqlite3.Error as e:
            print("SQLite error:", e)

    @staticmethod
    # Updating the database to add new columns
    def alter_tables_add_columns():
        try:
            # Connect to the SQLite3 database
            conn = sqlite3.connect(data_name)
            cursor = conn.cursor()

            # Add 'client_keywords' to Clients table
            cursor.execute("ALTER TABLE Clients ADD COLUMN client_keywords TEXT")

            # Add 'client_keywords' to Users table
            cursor.execute("ALTER TABLE Users ADD COLUMN client_keywords TEXT")

            # Commit changes and close connection
            conn.commit()
            conn.close()
            print("Database tables updated successfully.")

        except sqlite3.Error as e:
            print(f"Error updating database tables: {e}")
