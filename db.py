#####################
###### IMPORTS ######
#####################

import psycopg2
import ollama
from IPython.display import display_markdown, display_pretty

#####################
###### DATABASE #####
#####################

conn = psycopg2.connect("dbname=<> user=<> password=<> host=<>")

if (conn):
    print("Connected.")
else:
    print("Connection failed.")

cur = conn.cursor()

#####################
###### FUNCTIONS ####
#####################

def main():
    # Generate embeddings
    generate_embeddings()

    # Retrieve embeddings
    retrieve_embeddings()

    # Retrieve products
    retrieve_products()


def generate_embeddings():
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

    # Close connection
    conn.close()


def retrieve_embeddings():
    query = "SELECT products.id, products.name, products.description, embeddings.embedding FROM products JOIN embeddings ON products.id = embeddings.id"

    # Execute a query
    cur.execute(query)

    # Retrieve query results
    products = cur.fetchall()

    # Print the results
    for id, name, description, embedding in products:
        print(f"Id: {id}, Name: {name}, Description: {description}, Embedding: {embedding}")   

    # Close connection
    conn.close() 


def retrieve_products():
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
    products = cur.fetchall()

    # Print the results
    for id, name, description in products:
        print(f"Id: {id}, Name: {name}, Description: {description}")

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()