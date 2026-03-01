---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Commands for Copying Data to PostgreSQL on Docker"
subtitle: ""
summary: " "
tags: ["Docker","PostgreSQL"]
categories: ["Docker","PostgreSQL"]
url: docker-postgresql-copy-host-to-docker
date: 2022-10-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

### Preparation

Generate the target file. Loading MoneyForward household account detail data into PostgreSQL. Removing character encoding issues and unnecessary rows.

```sh
cat 収入・支出詳細_*.csv > import.csv
nkf -w --overwrite import.csv
sed -i '/計算対象/d' import.csv
sed -i -e "s/\"-/\"/g" import.csv
```

### Assumed Workflow: Copy File to Docker Host Then Execute

```sh
docker cp import.csv docker_postgres_1:/tmp/import.csv
docker exec docker_postgres_1 cat /tmp/import.csv

docker exec -it docker_postgres_1 psql -U postgres metabase -c "truncate table kakeibo"
docker exec -it docker_postgres_1 psql -U postgres metabase -c "COPY kakeibo FROM '/tmp/import.csv' with csv header encoding 'UTF8'"
```

### Notes

DDL memo

```sh

docker exec -it docker_postgres_1 psql -U postgres metabase

drop table kakeibo;
CREATE TABLE public.kakeibo (
    target_flg numeric,
    target_date date,
    item_detail text,
    ammount numeric,
    bank text,
    primary_item character varying(30),
    secondary_item character varying(30),
    item_memo text,
    transfer_flg numeric,
    item_id character varying(30)
);
```
