# pgvector
Open-source vector similarity search for Postgres - Postgres extension 
## Installation
Pull down docker image:
```
docker pull pgvector/pgvector:pg16
```
Run the docker container:
```
docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=your-password pgvector/pgvector:pg16
```
Execute shell inside container
```
docker exec -it mypostgres bash
```
Connect to PostgreSQL server
```
psql -h localhost -U postgres
```
Create database
```
CREATE DATABASE mydatabase;
```
List all the databases:
```
\l
```
Connect to database
```
\c mydatabase
```
