import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

class DatabaseUtils:

    def __init__(self, db_config):
        self.db_config = db_config

        try:
            self.connection = psycopg2.connect(**db_config)
        except Exception as e:
            print(f'Error connecting to the database: {e}')
            self.connection = None

    def schema_details(self, schema_name):
        schema_info_content = ""
        
        # Setting up the connection to use cursor
        connection = self.connection
        cursor = connection.cursor()
        schema_info_content = f"Database Schema: {schema_name}\n"

        try:            
            # Adding table name
            cursor.execute("SELECT table_name from information_schema.tables where table_schema = %s;", (schema_name,))
            table_list = cursor.fetchall()

            for table in table_list:
                table_name = table[0]
                schema_info_content = f"{schema_info_content}\n Table: {table_name}\n"

                # Addind columns and data tyoe
                cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s;", (table_name,))
                column_list = cursor.fetchall()

                for column in column_list:
                    column_name = column[0]
                    data_type = column[1]

                    schema_info_content = f"{schema_info_content} Column: {column_name}, Data Type: {data_type}\n"

                # # Adding Sample data
                cursor.execute(f"SELECT * from {schema_name}.{table_name} LIMIT 5")
                sample_data = cursor.fetchall()

                schema_info_content = f"{schema_info_content} Sample Data: \n"
                for row in sample_data:
                    schema_info_content = f"{schema_info_content}   {row}\n"
                
        except Exception as e:
            schema_info_content = f"Error fetching schema details: {e}"
            print(schema_info_content)

        finally:
            if cursor:  
                cursor.close()
            if connection:
                connection.close()

        return schema_info_content

    def execute_sql(self, query):
        try:
            connection = self.connection
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return str(result)
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()



obj = DatabaseUtils({
    "host": os.environ['host'],
    "port": int(os.environ['port']),
    "dbname": os.environ['database'],
    "user": os.environ['user'],
    "password": os.environ['password'],
})

res = obj.schema_details('public')

with open('test_schema_details.txt', 'w') as file:
    file.write(res)
        