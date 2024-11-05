# Building RAG with PostgreSQL using pgvector
`pgvector` Open-source vector similarity search for Postgres databases

## Setup database using CLI
- Pull down docker image:

```
docker pull pgvector/pgvector:pg16
```

- Run the docker container:

```
docker run -d --name pgtest -p 5432:5432 -e POSTGRES_PASSWORD=your-password pgvector/pgvector:pg16
```

- Execute shell inside container:

```
docker exec -it pgtest bash
```

- Connect to PostgreSQL server:

```
psql -h localhost -U postgres
```

- Create database (optional):

```sql
CREATE DATABASE mydatabase;
```

- List all the databases (optional):

```
\l
```

- Connect to database (optional):

```
\c mydatabase
```

### Store embeddings
- Create vector extension:

```tsql
CREATE EXTENSION vector;
```

- Create table with fields i.e, `id` and `embedding`:

```sql
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
```
> [!NOTE]
> Field `embedding` has the datatype as `vector` with **3** dimensions.
> Usually good embeddings model creates vectors with **1536** dimensions

- Create index using HNSW:

```sql
CREATE INDEX items_idx ON items USING hnsw (embedding vector_l2_ops);
```

- Get the indexes (optional):

```sql
SELECT * FROM pg_indexes WHERE schemaname='public';
```

- Insert values:

```sql
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
```

- Print values (optional):

```sql
SELECT * FROM items;
```

### Get distances
- Print `cosine distance` values as compared to `[1,2,3]`:

```sql
SELECT embedding <=> '[1,2,3]' AS cosine_distance FROM items;
```

- Print `cosine similarity` values as compared to `[1,2,3]`:

```sql
SELECT 1 - (embedding <=> '[1,2,3]') AS cosine_similarity FROM items;
```

### Retrieve embeddings
- Print embeddings using cosine distance operator `<=>`:

```sql
SELECT * FROM items ORDER BY embedding <=> '[1,2,3]' LIMIT 3;
```

- Print embeddings using euclidean distance operator `<->` (L2 distance):

```sql
SELECT * FROM items ORDER BY embedding <-> '[1,2,3]' LIMIT 3;
```

- Print embeddings using manhattan distance operator `<+>` (L1 distance):

```sql
SELECT * FROM items ORDER BY embedding <+> '[1,2,3]' LIMIT 3;
```

## Setup database using Python
0. Install [Python 3.12.5](https://www.python.org/downloads/).

    0.1. Install [Ollama](https://ollama.com/download) and pull down `mxbai-embed-large` using following command on Terminal:
   
    ```
    ollama pull mxbai-embed-large
    ```

    0.2. Install [Docker](https://www.docker.com/) and pull down docker image:

    ```
    docker pull pgvector/pgvector:pg16    
    ```

    0.3. Run the docker container:

    ```
    docker run -d --name pgtest -p 5432:5432 -e POSTGRES_PASSWORD=your-password pgvector/pgvector:pg16
    ```
   
1. Clone the repo
```
https://github.com/faranak-cs/pgvector-playground
```
2. Creat virtual envrionment
```
python3 -m venv venv
```
3. Activate virtual environment
```
source venv/bin/activate
```
4. Install packages
```
python -m pip install -r requirements.txt
```
5. Populate database
```
python db.py
```
6. Get relevant products
```
python db.py "clothes"
```

### Output
![pgvector-output](https://github.com/user-attachments/assets/e86ca4d5-df3f-4caa-8ff9-c7bf846866d6)


### Products (EXTRA)
- Get similar products when product with `id = 1` is out-of-stock:

```sql
SELECT * FROM products WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM products WHERE id = 1) LIMIT 5;
```

### Architecture Overview
![arch_overview](https://github.com/user-attachments/assets/9db06963-64c8-4707-b26a-9b061d8557e4)

## Useful Links
- Follow the repo below for more basic understanding:
    - https://github.com/pamelafox/pgvector-playground

