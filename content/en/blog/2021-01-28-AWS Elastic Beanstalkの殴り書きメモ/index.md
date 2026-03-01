---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Rough Notes on AWS Elastic Beanstalk"
subtitle: ""
summary: " "
tags: ["AWS","Elastic Beanstalk"]
categories: ["AWS","Elastic Beanstalk"]
url: aws-elastic-beanstalk-memo.html
date: 2021-01-28
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



# Introduction

![image-20210115220048472](image-20210115220048472.png)

First thing to note: the service name is "Elastic Beanstalk" - I tend to write it as "ElasticBeanStalk" or "Elastic Bean Stalk" so let me start there.

# Rough Notes

- A service for automating the setup of standard configurations and application deployments

- Components

  - Application
    - Top-level logical unit
    - Contains versions, environments, and environment configurations
  - Version
    - Deployable code
    - Version management on S3
    - Can deploy different versions to different environments
  - Environment
    - Infrastructure built for each environment
    - Deploy a version (source code)
      - Example Web server environment: ELB + EC2 (where code is deployed)
  - Environment Configuration
    - Configuration parameters that define the behavior of resources associated with the environment
      - Examples: EC2 instance type, Auto Scaling settings, etc.

- Environment Types

  - Load Balancing, Auto Scaling Environments
    - Run scalable web applications
      - High availability and elasticity
      - Web server environment: ELB + Auto Scaling
      - Worker environment: SQS + Auto Scaling
  - Single Instance Environments
    - For running batch applications
      - Single EC2 instance (Auto Scaling Max 1, Min 1)

- EB CLI

  - Installation

    ```
    [ec2-user@bastin ~]$ sudo pip3 install --upgrade awsebcli
    WARNING: pip is being invoked by an old script wrapper. This will fail in a future version of pip.
    Please see https://github.com/pypa/pip/issues/5599 for advice on fixing the underlying issue.
    To avoid this problem you can invoke Python with '-m pip' instead of running pip directly.
    Collecting awsebcli
      Downloading awsebcli-3.19.2.tar.gz (249 kB)
         |████████████████████████████████| 249 kB 14.3 MB/s
    Collecting botocore<1.20.0,>=1.19.0

    ```

  - Download Sample Code

    ```
    [ec2-user@bastin ~]$ git clone https://github.com/aws-samples/eb-node-express-sample.git
    Cloning into 'eb-node-express-sample'...
    remote: Enumerating objects: 8, done.
    remote: Counting objects: 100% (8/8), done.
    remote: Compressing objects: 100% (7/7), done.
    remote: Total 111 (delta 0), reused 2 (delta 0), pack-reused 103
    Receiving objects: 100% (111/111), 269.62 KiB | 496.00 KiB/s, done.
    Resolving deltas: 100% (34/34), done.
    ```

  - Create an Elastic Beanstalk Application

    ```
    [ec2-user@bastin eb-node-express-sample]$ eb init

    Select a default region
    1) us-east-1 : US East (N. Virginia)
    2) us-west-1 : US West (N. California)
    3) us-west-2 : US West (Oregon)
    4) eu-west-1 : EU (Ireland)
    5) eu-central-1 : EU (Frankfurt)
    6) ap-south-1 : Asia Pacific (Mumbai)
    7) ap-southeast-1 : Asia Pacific (Singapore)
    8) ap-southeast-2 : Asia Pacific (Sydney)
    9) ap-northeast-1 : Asia Pacific (Tokyo)
    10) ap-northeast-2 : Asia Pacific (Seoul)
    11) sa-east-1 : South America (Sao Paulo)
    12) cn-north-1 : China (Beijing)
    13) cn-northwest-1 : China (Ningxia)
    14) us-east-2 : US East (Ohio)
    15) ca-central-1 : Canada (Central)
    16) eu-west-2 : EU (London)
    17) eu-west-3 : EU (Paris)
    18) eu-north-1 : EU (Stockholm)
    19) eu-south-1 : EU (Milano)
    20) ap-east-1 : Asia Pacific (Hong Kong)
    21) me-south-1 : Middle East (Bahrain)
    22) af-south-1 : Africa (Cape Town)
    (default is 3): 9


    Select an application to use
    1) bel-dev-beanstalk-test
    2) [ Create new Application ]
    (default is 2):


    Enter Application Name
    (default is "eb-node-express-sample"):
    Application eb-node-express-sample has been created.

    It appears you are using Node.js. Is this correct?
    (Y/n): y
    Select a platform branch.
    1) Node.js 12 running on 64bit Amazon Linux 2
    2) Node.js 10 running on 64bit Amazon Linux 2
    3) Node.js running on 64bit Amazon Linux
    (default is 1):

    Do you wish to continue with CodeCommit? (Y/n): n
    Do you want to set up SSH for your instances?
    (Y/n): y

    Select a keypair.
    1) awskeypair
    2) DMSHandson58
    3) [ Create new KeyPair ]
    (default is 2): 1

    [ec2-user@bastin eb-node-express-sample]$

    ```

  - Create Environment and Deploy Code

    ```
    [ec2-user@bastin eb-node-express-sample]$ eb create
    Enter Environment Name
    (default is eb-node-express-sample-dev):
    Enter DNS CNAME prefix
    (default is eb-node-express-sample-dev):

    Select a load balancer type
    1) classic
    2) application
    3) network
    (default is 2):

    Would you like to enable Spot Fleet requests for this environment? (y/N): N
    ～omitted～
    ```



  - Deployment

    Deployment policies and settings - AWS Elastic Beanstalk https://docs.aws.amazon.com/ja_jp/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html

    - In Place Deployment (Rolling Deploy)

      - Uses instances from the current environment and applies new revision code
        - at once
        - Rolling

    - Blue/Green Deployment

      - Apply new revision code to new instances and swap the instances themselves

    - Deployment Configuration

      - Batch type: Number of instances to deploy at once
        - Percentage, fixed
      - Batch size: Number or percentage of instances to deploy in each batch

    - URL Swap

      - Deploy one version of an application, then deploy a new version as a different environment. Achieve Blue/Green Deployment by switching CNAMEs.

        > Trying out Elastic Beanstalk CNAME Swap | Developers.IO https://dev.classmethod.jp/articles/beanstalk-cname-swap/

    - Route53 Weighted Round Robin

      - Allows gradually testing new version code



  - Environment Configuration Customization

    - Specify options directly when creating the environment
    - Saved configurations
      - Save as configuration file in S3
        - eb config save
    - .ebextensions
      - Allows resource customization
        - Custom environment variables
        - Software installation
        - Software execution
        - Creating AWS resources not available by default

  - Monitoring

    - Basic health reporting
      - Environment health status
      - ELB health checks
      - CloudWatch metrics
    - Enhanced health reporting
      - OS-level metrics
      - Application-level metrics
