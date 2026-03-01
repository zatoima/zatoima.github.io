---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "AWS SysOps Administrator Associate Exam: Failure and Success Experience"
subtitle: ""
summary: " "
tags: ["AWS"]
categories: ["AWS"]
url: aws-sysops-certificate.html
date: 2019-09-16
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



This is my experience report of both failing and passing the AWS Certified SysOps Administrator - Associate exam. I want to document my reasons for failing to serve as a lesson for the future. If anyone reads this article, let it be a reminder to stay sharp and not be overconfident!

## Background

#### Skill Level

I already had the SAA (AWS Certified Solutions Architect - Associate) which I obtained in 2017. Personally, I mainly use AWS for test environments, and I only use it occasionally for work. I don't have extensive development experience.

#### Exam Prerequisites

The exam content was revised in the fall of 2018, and I naturally took the revised exam. (Took the exam in September 2019)

Before the revision (old exam), there was information online saying "If you pass the SAA (AWS Certified Solutions Architect - Associate), the SysOps exam is easy" and "SysOps was the easiest among the three Associate exams (Solution Architect, SysOps, DevOps)." Please don't take these claims at face value. You'll fail like I did.

## Results When Passing and Failing

#### Exam Report When Failing

![image-20191221222715518](image-20191221222715518.png)

#### Exam Report When Passing

![image-20191221222735895](image-20191221222735895.png)

<img src="image-20191221222750184.png" alt="image-20191221222750184" style="zoom:50%;" />

## About the Exam Scope

First, check the official site.

> AWS Certified SysOps Administrator - Associate https://aws.amazon.com/jp/certification/certified-sysops-admin-associate/
>
> ### Abilities Validated by the Certification
>
> - Deploy, manage, and operate scalable, highly available, and fault tolerant systems on AWS
> - Implement and control the flow of data to and from AWS
> - Select the appropriate AWS services based on compute, data, and security requirements
> - Identify appropriate use of AWS operational best practices
> - Estimate AWS usage costs and identify operational cost control mechanisms
> - Migrate on-premises workloads to AWS
>
> ### Recommended Knowledge
>
> - Understanding of AWS tenets (architectural design in the cloud)
> - Hands-on experience with AWS CLI and SDK/API tools
> - Understanding of networking technologies related to AWS
> - Understanding of security concepts and hands-on experience implementing security controls and compliance requirements
> - Understanding of virtualization technologies
> - Experience monitoring and auditing systems
> - Knowledge of networking concepts (DNS, TCP/IP, firewalls, etc.)
> - Ability to interpret architectural requirements

Looking at this page alone will leave you wondering "So what exactly should I study?", so look at the page below. It has the most comprehensive overview. (It's in English, but Google Translate works well enough.)

I found the following site when reconsidering my study method after failing once.

> AWS Certified SysOps Administrator - Associate (SOA-C01) Exam Learning Path | Jayendra's Blog http://jayendrapatil.com/aws-certified-sysops-administrator-associate-soa-c01-exam-learning-path/

Below are the areas I personally extracted as important from the above. I think the bold items in particular should be focused on.

#### 1.Monitoring & Management Tools

- **CloudWatch**
- **AWS Config**
- **AWS Systems Manager**
- **Trusted Advisor**
- Health Dashboard
- OpsWorks
- **CloudFormation**
- Beanstalk
- **CloudTrail**

#### 2.Networking & Content Delivery

- **VPC**
- **ELB**
- CloudFront
- Route53

#### 3.Compute

- **EC2**
- **Auto Scaling**
- Lambda
- API Gateway

#### 4.Storage

- **S3**
- **Glacier**
- **EBS**
- Storage Gateway
- EFS
- Snowball

#### 5.Databases

- **RDS**
- DynamoDB
- Aurora
- ElastiCache(Redis,Memcached)

#### 6.Security

- **IAM**
- KMS
- **Encryption**
- Inspector
- Shield
- WAF
- Artifact

#### 7.Integration Tools

- SQS
- SNS

#### 8.Cost management

- Organizations
- Consolidated billing
- billing Alert

That said, questions are truly spread across the board, so it's better to cover a wide range of topics broadly based on the URL above. I failed the first time, but I hadn't fully grasped the key points of the more detailed services mentioned above and fell short by a few percentage points.

## Exam Preparation

This may not be very helpful, but basically my first attempt was very casual. I thought just reading Blackbelt and FAQs would be enough.

### First Attempt

1. Read through Blackbelt (major services only - the bold services mentioned above)
2. Browse through the FAQs
3. Take the SysOps practice exam

After doing all this, as mentioned at the beginning, I charged into the exam believing the online reputation that "If you pass the SAA, SysOps is easy" and "SysOps was the easiest among the three Associate exams." (Failed miserably)

### Second Attempt

For the second attempt, I thought that understanding only the major services would make it difficult to reach a passing score, so I studied more broadly.

1. Read through Blackbelt (basically all of them)
2. Browse through the FAQs
3. Udemy practice exams (2 rounds)
4. SysOps practice exam (second time)
5. Practice with actual hands-on for areas I was unsure about

Interestingly, when I took the AWS practice exam again after a one-month gap, the questions had changed. **I'm not sure whether questions are randomized or if it was the timing of a practice exam refresh**, but if you have the budget, it might be worth taking it multiple times.

## For Those About to Take the Exam

- Don't let your guard down - study seriously.
- Develop a broad understanding of the services.
- Check the exam scope at the official site / Jayendra's Blog http://jayendrapatil.com/aws-certified-sysops-administrator-associate-soa-c01-exam-learning-path/

## Personal Thoughts

Honestly, my motivation for the first attempt was just to pass the exam. Not a very meaningful approach. Since I failed once, I then started actually using the services to understand them, which in a sense was a good thing.

I think it's rare to use everything in the certification exam scope in actual work, so the key is figuring out how to focus and efficiently study the relevant areas. (Especially for AWS exams)

Ah, I'm glad I passed. Next, I'm aiming for DevOps or SAA Pro!
