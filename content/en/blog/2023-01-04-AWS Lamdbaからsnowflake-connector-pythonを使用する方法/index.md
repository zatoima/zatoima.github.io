---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Notes on Using snowflake-connector-python in AWS Lambda"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: snowflake-connector-python-lambda-use
date: 2023-01-04
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

### Overview

Notes on the preparation required to use `snowflake-connector-python` in AWS Lambda.

### Methods for Using snowflake-connector-python in Lambda

There are three main approaches:

1. **Zip archive deployment** - Package the library with your Lambda function code
2. **Lambda Layer** - Create a shared layer containing the library
3. **Container image** - Use a Docker container image for the Lambda function

### Building for x86_64 on M1 Mac (arm64)

When developing on an M1 Mac (arm64 architecture), you need to cross-compile for Lambda's x86_64 architecture. Use the AWS SAM CLI build image for this purpose.

#### Using Docker with aws-sam-cli-build-image

```sh
# Pull the SAM CLI build image for Python 3.8 (x86_64)
docker pull amazon/aws-sam-cli-build-image-python3.8

# Run the container and install packages for x86_64
docker run --rm \
  -v $(pwd):/var/task \
  amazon/aws-sam-cli-build-image-python3.8 \
  pip install snowflake-connector-python -t /var/task/python/lib/python3.8/site-packages/
```

#### Create the Lambda Layer

```sh
# Zip the installed packages
cd python
zip -r ../snowflake-connector-layer.zip .
cd ..

# Upload to S3
aws s3 cp snowflake-connector-layer.zip s3://YOUR_BUCKET/

# Create Lambda Layer
aws lambda publish-layer-version \
  --layer-name snowflake-connector-python \
  --description "Snowflake Connector Python" \
  --content S3Bucket=YOUR_BUCKET,S3Key=snowflake-connector-layer.zip \
  --compatible-runtimes python3.8 \
  --compatible-architectures x86_64
```

### Sample Lambda Function

```python
import snowflake.connector
import os

def lambda_handler(event, context):
    conn = snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        database=os.environ['SNOWFLAKE_DATABASE'],
        schema=os.environ['SNOWFLAKE_SCHEMA']
    )

    try:
        cur = conn.cursor()
        cur.execute("SELECT CURRENT_VERSION()")
        result = cur.fetchone()
        return {
            'statusCode': 200,
            'body': f"Snowflake version: {result[0]}"
        }
    finally:
        conn.close()
```

### Addendum: Python 3.8 Deprecation

Note that Python 3.8 runtime for AWS Lambda has been deprecated. When creating new Lambda functions, use Python 3.10 or later.

When using a newer Python version, update the build image accordingly:

```sh
docker pull amazon/aws-sam-cli-build-image-python3.11
```

And update the `compatible-runtimes` parameter when creating the layer:
```sh
--compatible-runtimes python3.11
```
