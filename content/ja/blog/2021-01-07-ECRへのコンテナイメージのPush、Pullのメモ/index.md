---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ECRへのコンテナイメージのPush、Pullのメモ"
subtitle: ""
summary: " "
tags: ["AWS","ECR"]
categories: ["AWS","ECR"]
url: aws-ecr-container-push-pull
date: 2022-01-07
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

### ECRへのPush

```sh
mkdir aipine-docker
cd aipine-docker

cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk --update add ruby && rm -rf /var/cache/apk/*
EOF

docker build -t xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate .
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com
docker push xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate
aws ecr list-images --repository-name sample-fargate
```

### 実行ログ

```sh
[ec2-user@bastin ~]$ mkdir aipine-docker
[ec2-user@bastin ~]$ cd aipine-docker
[ec2-user@bastin aipine-docker]$ 
[ec2-user@bastin aipine-docker]$ cat > Dockerfile << 'EOF'
> FROM alpine:latest
> RUN apk --update add ruby && rm -rf /var/cache/apk/*
> EOF
[ec2-user@bastin aipine-docker]$ 
[ec2-user@bastin aipine-docker]$ docker build -t xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM alpine:latest
 ---> c059bfaa849c
Step 2/2 : RUN apk --update add ruby && rm -rf /var/cache/apk/*
 ---> Using cache
 ---> d5cd040a87f2
Successfully built d5cd040a87f2
Successfully tagged xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate:latest
[ec2-user@bastin aipine-docker]$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com
WARNING! Your password will be stored unencrypted in /home/ec2-user/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[ec2-user@bastin aipine-docker]$ docker push xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate
Using default tag: latest
The push refers to repository [xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate]
8a1cebaa0140: Pushed 
8d3ac3489996: Layer already exists 
latest: digest: sha256:40f2fd6d282ff49e0f0b7cb973df0f443338bcef6f40bdc20b578073d9945b18 size: 739
[ec2-user@bastin aipine-docker]$ aws ecr list-images --repository-name sample-fargate
{
    "imageIds": [
        {
            "imageDigest": "sha256:40f2fd6d282ff49e0f0b7cb973df0f443338bcef6f40bdc20b578073d9945b18",
            "imageTag": "latest"
        }
    ]
}
[ec2-user@bastin aipine-docker]$ 
```

### ECRからコンテナイメージをpullする

```sh
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com
docker pull xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate:latest
docker images
```

### 実行ログ

```sh
[ec2-user@bastin aipine-docker]$ aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com
WARNING! Your password will be stored unencrypted in /home/ec2-user/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
[ec2-user@bastin aipine-docker]$ docker images
REPOSITORY                                                         TAG       IMAGE ID       CREATED          SIZE
xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate   latest    d5cd040a87f2   11 minutes ago   20.1MB
alpine                                                             latest    c059bfaa849c   5 weeks ago      5.59MB
[ec2-user@bastin aipine-docker]$ 
[ec2-user@bastin aipine-docker]$ docker pull xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate:latest
latest: Pulling from sample-fargate
Digest: sha256:40f2fd6d282ff49e0f0b7cb973df0f443338bcef6f40bdc20b578073d9945b18
Status: Image is up to date for xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate:latest
xxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/sample-fargate:latest
```

