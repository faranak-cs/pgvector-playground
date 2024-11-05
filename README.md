# pgvector
Open-source vector similarity search for Postgres - Postgres extension 
## Create database
- Pull down docker image:

```
docker pull pgvector/pgvector:pg16
```

- Run the docker container:

```
docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=your-password pgvector/pgvector:pg16
```

- Execute shell inside container:

```
docker exec -it mypostgres bash
```

- Connect to PostgreSQL server:

```
psql -h localhost -U postgres
```

- Create database:

```sql
CREATE DATABASE mydatabase;
```

- List all the databases:

```
\l
```

- Connect to database:

```
\c mydatabase
```

## Store embeddings
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

- Insert values:

```sql
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
```

- Print values:

```sql
SELECT * FROM items;
```

## Get distances
- Print `cosine distance` values as compared to `[1,2,3]`:

```sql
SELECT embedding <=> '[1,2,3]' AS cosine_distance FROM items;
```

- Print `cosine similarity` values as compared to `[1,2,3]`:

```sql
SELECT 1 - (embedding <=> '[1,2,3]') AS cosine_similarity FROM items;
```

## Get embeddings
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

## Products
- Get similar products when product with `id = 1` is out-of-stock:

```sql
SELECT * FROM products WHERE id != 1 ORDER BY embedding <-> (SELECT embedding FROM products WHERE id = 1) LIMIT 5;
```

## Architecture Overview
![arch_overview](https://github.com/user-attachments/assets/9db06963-64c8-4707-b26a-9b061d8557e4)

