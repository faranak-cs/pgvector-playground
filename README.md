# pgvector
Open-source vector similarity search for Postgres - Postgres extension 
## Installation
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

## Embeddings
- Create vector extension:

```tsql
CREATE EXTENSION vector;
```

- Create table with fields i.e, `id` and `embedding` :

```sql
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
```
> [!NOTE]
> Field `embedding` has the datatype as `vector` with **3** dimensions.
> Usually good embeddings model creates vectors with **1536** dimensions

- Insert values:

```sql
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]'), ('[10,11,12]'), ('[13,14,15]');
```

- Print values:

```sql
SELECT * FROM items;
```









