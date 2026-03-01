---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Issuing an SSL Certificate with ACM Using a Domain Obtained from onamae.com"
subtitle: ""
summary: " "
tags: ["AWS","ACM"]
categories: ["AWS","ACM"]
url: aws-acm-ssl-certigication-setting
date: 2022-02-07
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, B
---

As the title suggests, these are notes on issuing an SSL certificate with ACM using a domain obtained from onamae.com.

### Request a Public Certificate from ACM

![image-20220112134641278](image-20220112134641278.png)

Enter the domain name and validation method

![image-20220112134754419](image-20220112134754419.png)

Certificate issuance in progress. Wait for a while.

![image-20220112134832140](image-20220112134832140.png)

Go to the certificate details screen, select "Export to CSV" and download it locally. You will need it for subsequent steps.

![image-20220112135511287](image-20220112135511287.png)

Go to onamae.com and navigate to "Set DNS Records"

![image-20220112135631643](image-20220112135631643.png)

Select the target domain and proceed to the next step

![image-20220112135711384](image-20220112135711384.png)

Use the DNS record settings

![image-20220112135824174](image-20220112135824174.png)

You should have downloaded a CSV like the one below from the ACM screen. Enter the following from it:

![image-20220112140655648](image-20220112140655648.png)

| Hostname    | TYPE  | VALUE        |
| ----------- | ----- | ------------ |
| Domain Name | CNAME | Record Value |

Enter the values and add them

![image-20220112140548910](image-20220112140548910.png)

Leave the settings at the bottom of the page as default and check them

![image-20220112140711412](image-20220112140711412.png)

Click "Set"

![image-20220112140751547](image-20220112140751547.png)

It is now complete.

![image-20220112140823966](image-20220112140823966.png)

It says DNS propagation can take a few hours to 24 hours, so be patient.

https://help.onamae.com/answer/8081

![image-20220112141220725](image-20220112141220725.png)

The status changed to "Issued" within a few dozen minutes.

![image-20220112142634611](image-20220112142634611.jpg)

### References

Troubleshoot a pending ACM certificate https://aws.amazon.com/jp/premiumsupport/knowledge-center/acm-certificate-pending-validation/
