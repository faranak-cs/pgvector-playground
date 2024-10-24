import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("dbname=<> user=<> password=<> host=<>")

if (conn):
    print("Connected.")
else:
    print("Connection failed.")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM items")

# Retrieve query results
records = cur.fetchall()

# Print the results
print(records)