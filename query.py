import psycopg2
import ollama
from IPython.display import display_markdown, display_pretty

# Connect to your postgres DB
conn = psycopg2.connect("dbname=<> user=<> password=<> host=<>")

if (conn):
    print("Connected.")
else:
    print("Connection failed.")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM products")

# Retrieve query results
products = cur.fetchall()

# Generate embeddings
for id, name, description in products:
    # Generate
    embedding = ollama.embeddings(model='mxbai-embed-large', prompt=(description))['embedding']
    # Store
    cur.execute("INSERT INTO embeddings (id, embedding) VALUES (%s, %s)", (id, embedding))
    # Commit
    conn.commit()

# Commit the changes
conn.commit()

# Retrieve embeddings
# query = "SELECT products.id, products.name, products.description, embeddings.embedding FROM products JOIN embeddings ON products.id = embeddings.id"
query = """
WITH temp AS (
    SELECT embedding
    FROM embeddings
    JOIN products 
    USING (id)
    WHERE products.name = 'Backpack'
)
    SELECT id, name, description
    FROM embeddings
    JOIN products
    USING (id)
    WHERE embedding <=> (SELECT embedding FROM temp) < 0.5;
"""

# Execute a query
cur.execute(query)

# Retrieve query results
# products = cur.fetchone()
products = cur.fetchall()

# Print the results
for id, name, description in products:
    print(f"Id: {id}, Name: {name}, Description: {description}")
# print(products)

# Close connection
conn.close()