# Useful commands for ClickHouse

## Create table

```clickhouse
docker exec -it clickhouse clickhouse-client --query="
CREATE TABLE example_table
  (
     uid String,
     gender_age String,
     timestamp Int64,
     url String
 )
 ENGINE = MergeTree()
 PARTITION BY toYYYYMM(toDate(timestamp/1000))
 PRIMARY KEY timestamp
 ORDER BY timestamp
 SETTINGS index_granularity = 8192
"
```

## Show tables
```docker
docker exec -it clickhouse clickhouse-client --query="show tables" 
```

## Select *
```docker
docker exec -it clickhouse clickhouse-client --query="select * from vl_lab02_rt" 
```

## Insert JSON data

```docker
cat lab02_train_exploded50.json | docker exec -i clickhouse clickhouse-client  --multiline --query="INSERT into example_table format JSONEachRow"
```

## Select data

```docker
docker exec -i clickhouse clickhouse-client --query="select count(uid) from my_table_gender_age_dist"

docker exec -i clickhouse clickhouse-client --query="select count(*) from example_table where timestamp=1419714194423"
```