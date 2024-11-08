#####################
###### IMPORTS ######
#####################

from get_embeddings import get_embeddings
import argparse
import psycopg2
# from IPython.display import display_markdown, display_pretty

#####################
###### DATABASE #####
#####################

conn = psycopg2.connect("dbname=postgres user=postgres password=admin123 host=localhost")

if (conn):
    print("Connected.")
else:
    print("Connection failed.")

cur = conn.cursor()

#####################
###### FUNCTIONS ####
#####################

def main():
    parser = argparse.ArgumentParser(description="Retrieve products using query")
    parser.add_argument("user_query", type=str, help="Query to retrieve products")
    args = parser.parse_args()
    user_query = args.user_query
    print(f"User query: {user_query}")

    # Retrieve products using user query
    retrieve_products_using_user_query(user_query)


def generate_embeddings():
    # Execute a query
    cur.execute("SELECT * FROM products")

    # Retrieve query results
    products = cur.fetchall()

    # Generate embeddings
    for id, name, description in products:
        # Generate
        embedding = get_embeddings(description)
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


def retrieve_products_using_name():
    # Retrieval based on cosine_similarity (1 - cosine_distance)
    query = """
        WITH temp AS (
            SELECT embedding
            FROM embeddings
            JOIN products 
            USING (id)
            WHERE products.name = 'Backpack'
        )
            SELECT id, name, description
            FROM products
            JOIN embeddings
            USING (id)
            WHERE 1 - (embedding <=> (SELECT embedding FROM temp)) > 0.55 LIMIT 5;
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


def retrieve_products_using_user_query(user_query):
    # Generate the embedding
    embedded_query = get_embeddings(user_query)
    # print(f"Embedded query: {embedded_query}")
    
    # Store the embedding
    # cur.execute("INSERT INTO users (user_query, embedded_query) VALUES (%s, %s)", (user_query, embedded_query))
    # Commit the changes
    # conn.commit()

    # Retrieval based on cosine_similarity (1 - cosine_distance)
    # query = f"""
    #     WITH temp AS (
    #         SELECT embedded_query
    #         FROM users
    #         WHERE user_query = %s
    #         LIMIT 1
    #     )
    #         SELECT id, name, description
    #         FROM products
    #         JOIN embeddings
    #         USING (id)
    #         WHERE 1 - (embedding <=> (SELECT embedded_query FROM temp)) > 0.45 
    #         LIMIT 5;
    # """

    query = """
        SELECT id, name, description
        FROM products
        JOIN embeddings
        USING (id)
        WHERE 1 - (embedding <=> %s::vector) > 0.5 
        LIMIT 5;
    """

    # Execute a query
    # cur.execute(query, (user_query,))
    cur.execute(query, (embedded_query,))

    # Retrieve query results
    products = cur.fetchall()

    # Print the results
    for id, name, description in products:
        print(f"Id: {id}, Name: {name}, Description: {description}")

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()