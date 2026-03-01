---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "GCP Associate Cloud Engineer Exam Guide - Setting Up Cloud Solution Environments"
subtitle: ""
summary: " "
tags: ["GCP"]
categories: ["GCP"]
url: gcp-associate-cloud-engineer-exam-guide-1
date: 2021-09-05
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only:

---




## Introduction

In preparation for the GCP Associate Cloud Engineer exam, I reviewed the manual contents described in the exam guide and verified some of them on actual equipment, studying according to the exam guide. The following five major topics are covered in the exam:

1. Setting up cloud solution environments
2. Planning and configuring a cloud solution
3. Deploying and implementing a cloud solution
4. Ensuring successful operation of a cloud solution
5. Configuring access and security

The [exam guide](https://cloud.google.com/certification/guides/cloud-engineer?hl=ja) further subdivides these major topics, and specific exam items are set as follows:

![image-20210904174227265](image-20210904174227265.png)

First, let's examine **Setting up cloud solution environments**.

## 1. Setting Up Cloud Solution Environments

### 1.1 Set up cloud projects and accounts. Tasks include:

- #### Creating a project

  > Reference: [Creating and Managing Projects \| Resource Manager Documentation \| Google Cloud](https://cloud.google.com/resource-manager/docs/creating-managing-projects?hl=ja&visit_id=637231726576722822-851915107&rd=1#creating_a_project)

A Google Cloud project is the basis for creating, enabling, and using all Google Cloud services, including managing APIs, enabling billing, adding and removing collaborators, and managing permissions for Google Cloud resources. For example, if you want to separate production and development environments, you would separate projects. In AWS, this corresponds to account separation, with IAM users created for each. Switching between environments (accounts) is done using IAM Switch Role. Personally, I find GCP's approach easier to understand.

##### Console

![image-20210904173925083](image-20210904173925083.png)

##### gcloud command

```
gcloud projects create PROJECT_ID
```

- #### Assigning users to predefined IAM roles within a project

  > Reference: [Managing Access to Projects, Folders, and Organizations \| Cloud IAM Documentation \| Google Cloud](https://cloud.google.com/iam/docs/granting-changing-revoking-access)
  - Select predefined roles to add from "IAM & Admin" > "IAM".

  ![image-20210904204946715](image-20210904204946715.png)

  - GCP IAM elements are as follows. Note that while similar words are used as in AWS, the contents are completely different.

    - Reference: [FAQ \| Cloud IAM Documentation \| Google Cloud](https://cloud.google.com/iam/docs/faq?hl=ja#roles_and_policies)

    - Member: The entity to which permissions are granted. Google Account, Service Account, Google Group, G Suite, Cloud Identity domain.

    - Role: A collection of permissions. When a role is granted to a member, all permissions in the role are granted.

      - Basic roles, predefined roles, and custom roles exist. Basic roles include Owner, Editor, and Viewer roles that affect all GCP services. Predefined roles are permission sets provided by GCP. Custom roles are permission sets configured by the user.

      - Basic roles have this note in the manual:

        > **Caution:** Basic roles include thousands of permissions across all Google Cloud services. In production environments, do not grant basic roles unless there is no alternative. Instead, grant the most limited [predefined role](https://cloud.google.com/iam/docs/understanding-roles?hl=ja#predefined_roles) or [custom role](https://cloud.google.com/iam/docs/understanding-custom-roles?hl=ja) that meets your needs.

      - AWS users may get confused, but GCP roles are equivalent to IAM policies in AWS.

    - Policy: Controls who (user) has what (role) permissions on which resource.

      - Similar to a bucket policy in AWS.

      - https://cloud.google.com/iam/docs/faq?hl=ja#what_does_an_policy_look_like

        ```
        {
          "bindings": [
           {
             "role": "roles/owner",
             "members": [
               "user:jiwoo@example.com",
               "group:admins@example.com",
               "domain:google.com",
               "serviceAccount:my-other-app@appspot.gserviceaccount.com"]
              },
              {
                "role": "roles/compute.networkViewer",
                "members": ["user:luis@example.com"]
              }
            ]
        }
        ```

- #### Managing users in Cloud Identity (manually and automated)

  - Since GCP is a Google service, Google Accounts can be used for GCP accounts. Organizations that cannot create Google Accounts or those using G Suite can manage accounts with Cloud Identity.

    > Reference: [Setup Instructions for GCP Administrators - Cloud Identity Help](https://support.google.com/cloudidentity/topic/7555414)

    > Cloud Identity is an Identity as a Service (IDaaS) and enterprise mobility management (EMM) solution. It provides the identity services and endpoint management available in Google Workspace as a standalone service. With Cloud Identity, administrators can manage users, apps, and devices from the Google Admin console.

  - Integration with the common Microsoft Active Directory is also supported.

    - [Federating Google Cloud with Active Directory: Introduction \| Architecture](https://cloud.google.com/solutions/federating-gcp-with-active-directory-introduction?hl=ja)

    ![Cloud Identity を使用した Active Directory の連携](https://cloud.google.com/solutions/images/federating-gcp-with-ad-with-cloud-identity.svg?hl=ja)

- #### Enabling APIs within projects

  - In GCP, you need to enable APIs for services you use. This can be done from the API Library screen or via gcloud.

    - Why is GCP designed to require API activation?
      - Inevitably leads to one-liners like this...
      - [One-liner to Enable All GCP APIs - Qiita](https://qiita.com/shiozaki/items/cd67c22c6408bc164dac)

    > Reference: [Enabling APIs in a Google Cloud Project \| Cloud Endpoints with OpenAPI](https://cloud.google.com/endpoints/docs/openapi/enable-api?hl=ja)

  - From the API Library

    ![image-20210904214003567](image-20210904214003567.png)

  - gcloud command

    ```
    gcloud services enable SERVICE_NAME
    ```

- #### Provisioning Stackdriver workspaces

  - Stackdriver has been integrated into the Operations Suite, and specifically provisioning workspaces is no longer required.
  - Operations Suite overview:
    - [Cloud Logging](https://cloud.google.com/logging?hl=ja)
      - Real-time log management and analysis
      - Can ingest application and system log data, as well as custom log data from GKE environments, VMs, and Google Cloud services
    - [Cloud Monitoring](https://cloud.google.com/monitoring?hl=ja)
      - Built-in large-scale metrics observability
      - Monitor performance, uptime, and overall behavior of applications running in the cloud. Collect metrics, events, and metadata from Google Cloud services, hosted uptime probes, application instrumentation, and commonly used application components, then visualize with charts and dashboards and manage alerts
    - Application Performance Management (APM)
      - Integrates [Cloud Trace](https://cloud.google.com/trace?hl=ja), [Cloud Debugger](https://cloud.google.com/debugger?hl=ja), and [Cloud Profiler](https://cloud.google.com/profiler?hl=ja)
      - Cloud Trace
        - Detect performance bottlenecks in production
          - Cloud Trace automatically analyzes all application traces and generates detailed latency reports that identify the causes of performance degradation
      - Cloud Debugger
        - Investigate code behavior in production
          - Real-time application debugging
      - Cloud Profiler
        - Continuous CPU and heap profiling to help improve performance and reduce costs

### 1.2 Manage billing configuration. Tasks include:

- #### Creating a billing account

  - Requires `billing.accounts.create` permission

    > Reference: [Create, Modify, or Close a Self-Serve Cloud Billing Account \| Cloud Billing \| Google Cloud](https://cloud.google.com/billing/docs/how-to/manage-billing-account?hl=ja#create_a_new_billing_account)

  ![image-20210904215058997](image-20210904215058997.png)

  ![image-20210904215130726](image-20210904215130726.png)

  ![image-20210904215147149](image-20210904215147149.png)

- #### Linking projects to a billing account

  > Reference: [Enable, Disable, or Change Billing for a Project \| Cloud Billing \| Google Cloud](https://cloud.google.com/billing/docs/how-to/modify-project?hl=ja#change_the_billing_account_for_a_project)

- #### Setting up billing budgets and alerts

  Reference: [Set Budgets and Budget Alerts \| Cloud Billing \| Google Cloud](https://cloud.google.com/billing/docs/how-to/budgets?hl=ja)

  ![image-20210904215700257](image-20210904215700257.png)

  ![image-20210904215721320](image-20210904215721320.png)

- #### Setting up billing exports to estimate daily/monthly charges

  - Using the Cloud Billing export to BigQuery feature, you can automatically export detailed Google Cloud billing data (usage, cost estimates, pricing data, etc.) to a specified BigQuery dataset throughout the day. Note that Cloud Billing data before enabling export will not be available.

    > Reference: [Export Cloud Billing Data to BigQuery \| Google Cloud](https://cloud.google.com/billing/docs/how-to/export-data-bigquery?hl=ja)

    ![image-20210904215946167](image-20210904215946167.png)

    ![image-20210904220002244](image-20210904220002244.png)

### 1.3 Install and configure the command-line interface (CLI), specifically Cloud SDK (e.g., setting the default project)

- When the manual says "SDK configuration," it's unclear what it refers to, but in English it appears to be "Configuration." I understand this as something like profiles or settings.

  - Create a configuration

    ```
    gcloud config configurations create [NAME]
    ```

  - Activate a configuration

    ```
    gcloud config configurations activate [NAME]
    ```

  - List configurations

    ```
    gcloud config configurations list
    ```

  - Set configuration properties

    ```
    gcloud config set project [PROJECT]
    gcloud config unset project
    ```

  - Display configuration properties

    ```
    gcloud config configurations describe [NAME]
    ```

  - Delete a configuration

    ```
    gcloud config configurations delete [NAME]
    ```

  Reference: [Managing SDK Configurations \| Cloud SDK Documentation \| Google Cloud](https://cloud.google.com/sdk/docs/configurations?hl=ja)
