```bash
docker exec -it spark-master spark-submit --master spark://spark-master:7077 jobs/main.py --packages org.apache.paimon:paimon-spark-3.5:1.3.1
```

# Apache Flink + Apache Paimon + MinIO Integration + CDC from Postgres


A complete Docker-based setup demonstrating how to use **Apache Flink** to write data to **MinIO** (S3-compatible storage) using **Apache Paimon** as a lakehouse storage format. This project solves the dependency hell that often occurs when trying to integrate these components together.

## 🚀 What's Inside

- **Apache Flink 1.19.3** - Stream processing framework
- **Apache Paimon 1.2.0** - Stream Lakehouse storage format with ACID transactions
- **MinIO (latest)** - S3-compatible object storage
- **Spark 3.5.0** - batch processing framework

## 🛠️ Quick Start

### 1. Build and Start the Services

```bash
# Build the custom Flink image with embedded JARs
docker compose build --no-cache

# Start all services (MinIO, Flink JobManager, Flink TaskManager)
docker compose up -d
```

### 2. Verify Everything is Running

- **Flink Web UI**: http://localhost:8081
- **MinIO Console**: http://localhost:9001 (admin/password)
- **MinIO API**: http://localhost:9000
- **Spark History**: http://localhost:4040 (Spark History Server)
- **Postgres**: port 5522 (user/pw)


### 2.1 Prepare Postgres
```sql
-- create schema
create schema flink;

-- Create user 
create user cdc_user with replication password 'cdc_pass';

-- Grant select
grant select on all tables in schema flink to cdc_user;
grant usage on schema flink to cdc_user;

-- create publication manualy
create publication dbz_publication for table flink.user_log;

-- create table in schema
create table flink.user_log(
    id serial primary key,
    name text,
    salary numeric(5,2),
    value int,
    active bool);
```

### 3. Connect to Flink SQL Client

```bash
docker exec -it flink-jobmanager /opt/flink/bin/sql-client.sh embedded
```

### 4. Create Streaming Pipeline

Once in the Flink SQL client, run these commands:

```sql
-- Create CDC Table in default catalog
USE CATALOG default_catalog;

CREATE TABLE user_log (
  id INT,
  name STRING,
  salary FLOAT,
  `value` INT,
  active BOOLEAN,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'postgres-cdc',
  'hostname' = '172.18.0.2',
  'port' = '5432',
  'username' = 'cdc_user',
  'password' = 'cdc_pass',
  'database-name' = 'local',
  'schema-name' = 'flink',
  'table-name' = 'user_log',
  'slot.name' = 'flink_cdc',
  'debezium.publication.autocreate.mode' = 'disabled',
  'debezium.slot.drop.on.stop' = 'true',
  'scan.startup.mode' = 'initial',
  'decoding.plugin.name' = 'pgoutput'
);


-- Create the Paimon catalog pointing to MinIO
CREATE CATALOG paimon_catalog WITH (
   'type' = 'paimon',
   'warehouse' = 's3://warehouse/paimon/',
   's3.endpoint' = 'http://minio:9000',
   's3.access-key' = 'admin',
   's3.secret-key' = 'password',
   's3.path.style.access' = 'true'
);

-- Switch to the Paimon catalog
USE CATALOG paimon_catalog;

-- Create a database
CREATE DATABASE flink;
USE flink;

-- Create table for Paimon
CREATE TABLE flink.user_log (
    id INT,
    `name` STRING,
    salary FLOAT,
    `value` INT,
    active BOOLEAN,
    PRIMARY KEY (id) NOT ENFORCED
);

-- Set execution params
SET 'execution.runtime-mode' = 'streaming';
SET 'execution.checkpointing.interval' = '10s';

-- Run Pipeline
INSERT INTO paimon_catalog.flink.user_log
SELECT * FROM  default_catalog.default_database.user_log;
```

## 5 Insert data to postgres and check data in paimon
```sql
insert into flink.user_log("name", "salary", "value", "active") values ('rols', 375.67, 1200, true);
insert into flink.user_log("name", "salary", "value", "active") values ('frel', 300.67, 1300, true);
insert into flink.user_log("name", "salary", "value", "active") values ('bbr', 250.67, 1100, true);

insert into flink.user_log("name", "salary", "value", "active") values ('cccr', 150.67, 900, true);
```

## 6 Manage queries in postgres
```sql
select * from pg_catalog.pg_replication_slots;

select pg_drop_replication_slot('');
```
## 📊 What You'll See

- Your INSERT job will appear in the Flink Web UI and complete successfully
- Data files will be created in MinIO under the `/warehouse/paimon/` path
- Paimon maintains full ACID properties with snapshots, manifests, and schema evolution support


## 🧹 Cleanup

```bash
# Stop all services
docker compose down

# Remove volumes (if you want to start fresh)
docker compose down -v
```
