import psycopg2

# Replace these with your database credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Menuchu"
DB_USER = "namsengi11"
DB_PASSWORD = "1234qwer"

try:
    # Establish a connection to the database
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")

# Close the connection
finally:
    if connection:
        connection.close()
