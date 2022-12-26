---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "parquet-toolsのインストール、及び操作方法のメモ"
subtitle: ""
summary: " "
tags: ["その他"]
categories: ["その他"]
url: parquet-tools-how-to-install-and-operate
date: 2021-11-02
featured: false
draft: false

# Featured image

---



## インストール

### maven、javaのインストール確認

```sh
[ec2-user@bastin ~]$ mvn -version
Apache Maven 3.5.2 (138edd61fd100ec658bfa2d307c43b76940a5d7d; 2017-10-18T07:58:13Z)
Maven home: /usr/share/apache-maven
Java version: 1.8.0_302, vendor: Red Hat, Inc.
Java home: /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.302.b08-0.amzn2.0.1.x86_64/jre
Default locale: en_US, platform encoding: UTF-8
OS name: "linux", version: "4.14.248-189.473.amzn2.x86_64", arch: "amd64", family: "unix"
```

### 資材のインストール

```sh
[ec2-user@bastin ~]$ mkdir parquet
[ec2-user@bastin ~]$ cd parquet/
[ec2-user@bastin parquet]$ git clone https://github.com/apache/parquet-mr.git
Cloning into 'parquet-mr'...
remote: Enumerating objects: 68629, done.
remote: Counting objects: 100% (1532/1532), done.
remote: Compressing objects: 100% (835/835), done.
remote: Total 68629 (delta 595), reused 1163 (delta 394), pack-reused 67097
Receiving objects: 100% (68629/68629), 17.45 MiB | 18.62 MiB/s, done.
Resolving deltas: 100% (40079/40079), done.
[ec2-user@bastin parquet]$ cd ./parquet-mr/parquet-tools/
-bash: cd: ./parquet-mr/parquet-tools/: No such file or directory
[ec2-user@bastin parquet]$ cd ./parquet-mr/
[ec2-user@bastin parquet-mr]$ ls -l
total 156
-rwxrwxr-x 1 ec2-user ec2-user  2178 Oct 20 10:12 changelog.sh
-rw-rw-r-- 1 ec2-user ec2-user 84314 Oct 20 10:12 CHANGES.md
drwxrwxr-x 2 ec2-user ec2-user   209 Oct 20 10:12 dev
drwxrwxr-x 3 ec2-user ec2-user    26 Oct 20 10:12 doc
-rw-rw-r-- 1 ec2-user ec2-user 11626 Oct 20 10:12 LICENSE
-rw-rw-r-- 1 ec2-user ec2-user  3569 Oct 20 10:12 NOTICE
drwxrwxr-x 3 ec2-user ec2-user    32 Oct 20 10:12 parquet-arrow
drwxrwxr-x 3 ec2-user ec2-user    69 Oct 20 10:12 parquet-avro
drwxrwxr-x 3 ec2-user ec2-user    63 Oct 20 10:12 parquet-benchmarks
-rw-rw-r-- 1 ec2-user ec2-user  9486 Oct 20 10:12 parquet_cascading.md
drwxrwxr-x 3 ec2-user ec2-user    49 Oct 20 10:12 parquet-cli
drwxrwxr-x 3 ec2-user ec2-user    52 Oct 20 10:12 parquet-column
drwxrwxr-x 3 ec2-user ec2-user    52 Oct 20 10:12 parquet-common
drwxrwxr-x 3 ec2-user ec2-user    52 Oct 20 10:12 parquet-encoding
drwxrwxr-x 3 ec2-user ec2-user    32 Oct 20 10:12 parquet-format-structures
drwxrwxr-x 3 ec2-user ec2-user    52 Oct 20 10:12 parquet-generator
drwxrwxr-x 3 ec2-user ec2-user    69 Oct 20 10:12 parquet-hadoop
drwxrwxr-x 3 ec2-user ec2-user    46 Oct 20 10:12 parquet-hadoop-bundle
drwxrwxr-x 3 ec2-user ec2-user    49 Oct 20 10:12 parquet-jackson
drwxrwxr-x 3 ec2-user ec2-user    52 Oct 20 10:12 parquet-pig
drwxrwxr-x 3 ec2-user ec2-user    32 Oct 20 10:12 parquet-pig-bundle
drwxrwxr-x 3 ec2-user ec2-user    69 Oct 20 10:12 parquet-protobuf
drwxrwxr-x 3 ec2-user ec2-user    32 Oct 20 10:12 parquet-scala
drwxrwxr-x 3 ec2-user ec2-user    69 Oct 20 10:12 parquet-thrift
-rw-rw-r-- 1 ec2-user ec2-user 23053 Oct 20 10:12 pom.xml
-rw-rw-r-- 1 ec2-user ec2-user  3049 Oct 20 10:12 PoweredBy.md
-rw-rw-r-- 1 ec2-user ec2-user 10418 Oct 20 10:12 README.md
drwxrwxr-x 2 ec2-user ec2-user    25 Oct 20 10:12 src
[ec2-user@bastin parquet-mr]$ git checkout apache-parquet-1.10.1
Note: switching to 'apache-parquet-1.10.1'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at a89df8f99 [maven-release-plugin] prepare release apache-parquet-1.10.1
```

### ビルド

```sh
[ec2-user@bastin parquet-mr]$ cd parquet-tools/
[ec2-user@bastin parquet-tools]$ mvn clean package -Plocal
[INFO] Scanning for projects...
[INFO] 
[INFO] -----------------------------------------------------------

～中略～

[WARNING] See http://docs.codehaus.org/display/MAVENUSER/Shade+Plugin
[INFO] Replacing original artifact with shaded artifact.
[INFO] Replacing /home/ec2-user/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar with /home/ec2-user/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1-shaded.jar
[INFO] Dependency-reduced POM written at: /home/ec2-user/parquet/parquet-mr/parquet-tools/dependency-reduced-pom.xml
[INFO] Dependency-reduced POM written at: /home/ec2-user/parquet/parquet-mr/parquet-tools/dependency-reduced-pom.xml
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 22.757 s
[INFO] Finished at: 2021-10-20T01:13:55Z
[INFO] Final Memory: 35M/377M
[INFO] ------------------------------------------------------------------------
[ec2-user@bastin parquet-tools]$ 
[ec2-user@bastin parquet-tools]$ ls -l
total 20
-rw-rw-r--  1 ec2-user ec2-user 3172 Oct 20 10:13 dependency-reduced-pom.xml
-rw-rw-r--  1 ec2-user ec2-user 4306 Oct 20 10:12 pom.xml
-rw-rw-r--  1 ec2-user ec2-user 2354 Oct 20 10:12 README.md
-rw-rw-r--  1 ec2-user ec2-user  979 Oct 20 10:12 REVIEWERS.md
drwxrwxr-x  4 ec2-user ec2-user   30 Oct 20 10:12 src
drwxrwxr-x 10 ec2-user ec2-user  304 Oct 20 10:13 target
[ec2-user@bastin parquet-tools]$ cd target/
[ec2-user@bastin target]$ ls -l
total 42332
drwxrwxr-x 4 ec2-user ec2-user       33 Oct 20 10:13 classes
drwxrwxr-x 3 ec2-user ec2-user       25 Oct 20 10:13 generated-sources
drwxrwxr-x 3 ec2-user ec2-user       30 Oct 20 10:13 generated-test-sources
drwxrwxr-x 2 ec2-user ec2-user       28 Oct 20 10:13 maven-archiver
drwxrwxr-x 3 ec2-user ec2-user       35 Oct 20 10:13 maven-status
-rw-rw-r-- 1 ec2-user ec2-user    81190 Oct 20 10:13 original-parquet-tools-1.10.1.jar
-rw-rw-r-- 1 ec2-user ec2-user 43242062 Oct 20 10:13 parquet-tools-1.10.1.jar
-rw-rw-r-- 1 ec2-user ec2-user    11045 Oct 20 10:13 parquet-tools-1.10.1-tests.jar
-rw-rw-r-- 1 ec2-user ec2-user     3124 Oct 20 10:13 rat.txt
drwxrwxr-x 2 ec2-user ec2-user        6 Oct 20 10:13 surefire
drwxrwxr-x 2 ec2-user ec2-user     4096 Oct 20 10:13 surefire-reports
drwxrwxr-x 3 ec2-user ec2-user       17 Oct 20 10:13 test-classes
[ec2-user@bastin target]$ 
```

## parquet-toolsの操作方法

### 中身の確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar cat testdata.parquet

id = 1
name = test1
comment = ゎ

id = 2
name = test2
comment = が

id = 3
name = test3
comment = ス
```

### メタ情報の確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar meta testdata.parquet
file:        file:/home/ec2-user/pyarrow/testdata.parquet 
creator:     parquet-cpp-arrow version 5.0.0 
extra:       pandas = {"index_columns": [{"kind": "range", "name": null, "start": 0, "stop": 3, "step": 1}], "column_indexes": [{"name": null, "field_name": null, "pandas_type": "unicode", "numpy_type": "object", "metadata": {"encoding": "UTF-8"}}], "columns": [{"name": "id", "field_name": "id", "pandas_type": "int64", "numpy_type": "int64", "metadata": null}, {"name": "name", "field_name": "name", "pandas_type": "unicode", "numpy_type": "object", "metadata": null}, {"name": "comment", "field_name": "comment", "pandas_type": "unicode", "numpy_type": "object", "metadata": null}], "creator": {"library": "pyarrow", "version": "5.0.0"}, "pandas_version": "1.0.5"} 
extra:       ARROW:schema = /////5ADAAAQAAAAAAAKAA4ABgAFAAgACgAAAAABBAAQAAAAAAAKAAwAAAAEAAgACgAAALwCAAAEAAAAAQAAAAwAAAAIAAwABAAIAAgAAAAIAAAAEAAAAAYAAABwYW5kYXMAAIUCAAB7ImluZGV4X2NvbHVtbnMiOiBbeyJraW5kIjogInJhbmdlIiwgIm5hbWUiOiBudWxsLCAic3RhcnQiOiAwLCAic3RvcCI6IDMsICJzdGVwIjogMX1dLCAiY29sdW1uX2luZGV4ZXMiOiBbeyJuYW1lIjogbnVsbCwgImZpZWxkX25hbWUiOiBudWxsLCAicGFuZGFzX3R5cGUiOiAidW5pY29kZSIsICJudW1weV90eXBlIjogIm9iamVjdCIsICJtZXRhZGF0YSI6IHsiZW5jb2RpbmciOiAiVVRGLTgifX1dLCAiY29sdW1ucyI6IFt7Im5hbWUiOiAiaWQiLCAiZmllbGRfbmFtZSI6ICJpZCIsICJwYW5kYXNfdHlwZSI6ICJpbnQ2NCIsICJudW1weV90eXBlIjogImludDY0IiwgIm1ldGFkYXRhIjogbnVsbH0sIHsibmFtZSI6ICJuYW1lIiwgImZpZWxkX25hbWUiOiAibmFtZSIsICJwYW5kYXNfdHlwZSI6ICJ1bmljb2RlIiwgIm51bXB5X3R5cGUiOiAib2JqZWN0IiwgIm1ldGFkYXRhIjogbnVsbH0sIHsibmFtZSI6ICJjb21tZW50IiwgImZpZWxkX25hbWUiOiAiY29tbWVudCIsICJwYW5kYXNfdHlwZSI6ICJ1bmljb2RlIiwgIm51bXB5X3R5cGUiOiAib2JqZWN0IiwgIm1ldGFkYXRhIjogbnVsbH1dLCAiY3JlYXRvciI6IHsibGlicmFyeSI6ICJweWFycm93IiwgInZlcnNpb24iOiAiNS4wLjAifSwgInBhbmRhc192ZXJzaW9uIjogIjEuMC41In0AAAADAAAAcAAAADAAAAAEAAAArP///wAAAQUQAAAAGAAAAAQAAAAAAAAABwAAAGNvbW1lbnQA2P///9T///8AAAEFEAAAABwAAAAEAAAAAAAAAAQAAABuYW1lAAAAAAQABAAEAAAAEAAUAAgABgAHAAwAAAAQABAAAAAAAAECEAAAABwAAAAEAAAAAAAAAAIAAABpZAAACAAMAAgABwAIAAAAAAAAAUAAAAA= 

file schema: schema 
--------------------------------------------------------------------------------
id:          OPTIONAL INT64 R:0 D:1
name:        OPTIONAL BINARY O:UTF8 R:0 D:1
comment:     OPTIONAL BINARY O:UTF8 R:0 D:1

row group 1: RC:3 TS:271 OFFSET:4 
--------------------------------------------------------------------------------
id:           INT64 UNCOMPRESSED DO:4 FPO:42 SZ:109/109/1.00 VC:3 ENC:PLAIN_DICTIONARY,RLE,PLAIN ST:[min: 1, max: 3, num_nulls: 0]
name:         BINARY UNCOMPRESSED DO:205 FPO:246 SZ:86/86/1.00 VC:3 ENC:PLAIN_DICTIONARY,RLE,PLAIN ST:[min: test1, max: test3, num_nulls: 0]
comment:      BINARY UNCOMPRESSED DO:361 FPO:396 SZ:76/76/1.00 VC:3 ENC:PLAIN_DICTIONARY,RLE,PLAIN ST:[min: が, max: ス, num_nulls: 0]
[ec2-user@bastin pyarrow]$ 
```

### スキーマ情報の確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar schema testdata.parquet

message schema {
  optional int64 id;
  optional binary name (UTF8);
  optional binary comment (UTF8);
}
```

### ダンプ

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar dump testdata.parquet
row group 0 
--------------------------------------------------------------------------------
id:       INT64 UNCOMPRESSED DO:4 FPO:42 SZ:109/109/1.00 VC:3 ENC:RLE, [more]...
name:     BINARY UNCOMPRESSED DO:205 FPO:246 SZ:86/86/1.00 VC:3 ENC:RL [more]...
comment:  BINARY UNCOMPRESSED DO:361 FPO:396 SZ:76/76/1.00 VC:3 ENC:RL [more]...

    id TV=3 RL=0 DL=1 DS:      3 DE:PLAIN_DICTIONARY
    ----------------------------------------------------------------------------
    page 0:                     DLE:RLE RLE:RLE VLE:PLAIN_DICTIONARY S [more]... VC:3

    name TV=3 RL=0 DL=1 DS:    3 DE:PLAIN_DICTIONARY
    ----------------------------------------------------------------------------
    page 0:                     DLE:RLE RLE:RLE VLE:PLAIN_DICTIONARY S [more]... VC:3

    comment TV=3 RL=0 DL=1 DS: 3 DE:PLAIN_DICTIONARY
    ----------------------------------------------------------------------------
    page 0:                     DLE:RLE RLE:RLE VLE:PLAIN_DICTIONARY S [more]... VC:3

INT64 id 
--------------------------------------------------------------------------------
*** row group 1 of 1, values 1 to 3 *** 
value 1: R:0 D:1 V:1
value 2: R:0 D:1 V:2
value 3: R:0 D:1 V:3

BINARY name 
--------------------------------------------------------------------------------
*** row group 1 of 1, values 1 to 3 *** 
value 1: R:0 D:1 V:test1
value 2: R:0 D:1 V:test2
value 3: R:0 D:1 V:test3

BINARY comment 
--------------------------------------------------------------------------------
*** row group 1 of 1, values 1 to 3 *** 
value 1: R:0 D:1 V:ゎ
value 2: R:0 D:1 V:が
value 3: R:0 D:1 V:ス
[ec2-user@bastin pyarrow]$ 
```

### 行数の確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar rowcount testdata.parquet
Total RowCount: 3
```

### サイズ確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar size testdata.parquet
Total Size: 271 bytes
```

### マージ

仮にこんな感じにパーティションごとに分かれているparquetがあったとして、、、

```sh
[ec2-user@bastin pyarrow]$ find pq -type f
pq/id=1/ad317ec807644ad98298860e7fb9d041.snappy.parquet
pq/id=2/ad317ec807644ad98298860e7fb9d041.snappy.parquet
pq/id=3/ad317ec807644ad98298860e7fb9d041.snappy.parquet
```

一つのファイルには1行程度のサイズしかないとする(こんな分割方法はありえないけども・・・)

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar cat pq/id=1/ad317ec807644ad98298860e7fb9d041.snappy.parquet
name = test1
comment = ゎぶばあちあぬナクバ
```

下記でマージ

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar merge pq/id=1/ad317ec807644ad98298860e7fb9d041.snappy.parquet pq/id=2/ad317ec807644ad98298860e7fb9d041.snappy.parquet pq/id=3/ad317ec807644ad98298860e7fb9d041.snappy.parquet merge.pq
Warning: file pq/id=1/ad317ec807644ad98298860e7fb9d041.snappy.parquet is too small, length: 1899
Warning: file pq/id=2/ad317ec807644ad98298860e7fb9d041.snappy.parquet is too small, length: 1899
Warning: file pq/id=3/ad317ec807644ad98298860e7fb9d041.snappy.parquet is too small, length: 1899
Warning: you merged too small files. Although the size of the merged file is bigger, it STILL contains small row groups, thus you don't have the advantage of big row groups, which usually leads to bad query performance!
```

### catで確認

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar cat  merge.pq
name = test1
comment = ゎぶばあちあぬナクバ

name = test2
comment = がマうひバぴじクハぺ

name = test3
comment = スみでてゥあッあけげ
```

### ヘルプ

```sh
[ec2-user@bastin pyarrow]$ java -jar $HOME/parquet/parquet-mr/parquet-tools/target/parquet-tools-1.10.1.jar help
Unknown command: help

parquet-tools cat:
Prints the content of a Parquet file. The output contains only the data, no
metadata is displayed
usage: parquet-tools cat [option...] <input>
where option is one of:
       --debug     Enable debug output
    -h,--help      Show this help string
    -j,--json      Show records in JSON format.
       --no-color  Disable color output even if supported
where <input> is the parquet file to print to stdout

parquet-tools head:
Prints the first n record of the Parquet file
usage: parquet-tools head [option...] <input>
where option is one of:
       --debug          Enable debug output
    -h,--help           Show this help string
    -n,--records <arg>  The number of records to show (default: 5)
       --no-color       Disable color output even if supported
where <input> is the parquet file to print to stdout

parquet-tools schema:
Prints the schema of Parquet file(s)
usage: parquet-tools schema [option...] <input>
where option is one of:
    -d,--detailed  Show detailed information about the schema.
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the parquet file containing the schema to show

parquet-tools meta:
Prints the metadata of Parquet file(s)
usage: parquet-tools meta [option...] <input>
where option is one of:
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the parquet file to print to stdout

parquet-tools dump:
Prints the content and metadata of a Parquet file
usage: parquet-tools dump [option...] <input>
where option is one of:
    -c,--column <arg>  Dump only the given column, can be specified more than
                       once
    -d,--disable-data  Do not dump column data
       --debug         Enable debug output
    -h,--help          Show this help string
    -m,--disable-meta  Do not dump row group and page metadata
    -n,--disable-crop  Do not crop the output based on console width
       --no-color      Disable color output even if supported
where <input> is the parquet file to print to stdout

parquet-tools merge:
Merges multiple Parquet files into one. The command doesn't merge row groups,
just places one after the other. When used to merge many small files, the
resulting file will still contain small row groups, which usually leads to bad
query performance.
usage: parquet-tools merge [option...] <input> [<input> ...] <output>
where option is one of:
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the source parquet files/directory to be merged
   <output> is the destination parquet file

parquet-tools rowcount:
Prints the count of rows in Parquet file(s)
usage: parquet-tools rowcount [option...] <input>
where option is one of:
    -d,--detailed  Detailed rowcount of each matching file
       --debug     Enable debug output
    -h,--help      Show this help string
       --no-color  Disable color output even if supported
where <input> is the parquet file to count rows to stdout

parquet-tools size:
Prints the size of Parquet file(s)
usage: parquet-tools size [option...] <input>
where option is one of:
    -d,--detailed      Detailed size of each matching file
       --debug         Enable debug output
    -h,--help          Show this help string
       --no-color      Disable color output even if supported
    -p,--pretty        Pretty size
    -u,--uncompressed  Uncompressed size
where <input> is the parquet file to get size & human readable size to stdout

```

