---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Rough Notes on FIWARE"
subtitle: ""
summary: " "
tags: ["fiware"]
categories: ["fiware"]
url: fiware-about-memo
date: 2021-12-04
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



### What is FIWARE

FIWARE is a data management platform focused on cross-domain data distribution, often referred to as a "City OS" for smart cities.

As the term "data management platform" implies, it is not just infrastructure — it appears capable of building many of the elements needed for data management on a component-by-component basis.

It seems to support core components, CKAN for handling data catalogs, Grafana for data visualization, and more. It also has the ability to receive and visualize data from IoT devices. The central hub for data exchange is the Context Broker, which enables Pub/Sub-style data communication. The component responsible for this role is called Orion.

Ultimately, it is a system capable of generating, collecting, publishing, and consuming information about cities. But why the emphasis on cities?

### Significance

Not limited to City OS, the lack of unified standards for inter-system integration can be a problem in general. While the US has large platform companies that are increasingly creating data silos, there is a perspective that Europe, Japan, and others are trying to build ecosystems through open source and standards like NGSI in FIWARE. The goal is to unify standards for data collection and accumulation, creating an ecosystem for mutual prosperity.

The term "ecosystem" in this context refers to a framework where multiple companies form partnerships in product development and business activities, leveraging each other's technologies and capital to coexist and thrive across industry boundaries and national borders.

### What FIWARE Enables

- Interoperability
- Data distribution
- Extensibility

DMBOK is a useful reference when it comes to data utilization and handling. DMBOK describes metadata management, data integration, interoperability, data modeling, data architecture, and other areas related to data governance. FIWARE appears to be partially effective for these areas as well. When integrating with various systems, you normally need to consider data modeling aspects such as how to share data, what formats to use, and what file types to adopt. FIWARE provides a defined framework that handles much of this.

- NGSI data model
- Open API
- Common API

Data exchange is conducted using the international standard called NGSI (Next Generation Service Interfaces), which was apparently drafted by Japan (though the standardization itself was done by a European organization).

NGSI defines interfaces for data integration and data models for data storage. The data model consists of "entities" and their attribute information called context information, enabling data integration between different applications. The data semantics follow FIWARE Data Models.

### How to Learn

To be honest, researching this on my own did not give me a clear understanding, so the quickest way to learn seems to be working through the following tutorial:

https://github.com/FIWARE/tutorials.Getting-Started/blob/master/README.ja.md

### References

- [Initiatives for Public-Private Data Utilization Common Platforms](https://www.sci-japan.or.jp/vc-files/member/secure/speakers/20201130.pdf?utm_source=pocket_mylist)
- [Open Source Software for Smart Cities: Getting Started with FIWARE](https://www.slideshare.net/ShunsukeKikuchi1/oss-fiware?utm_source=pocket_mylist)
- [NGSI v2 Summary - Qiita](https://qiita.com/NKGWM/items/603bc49da608a12d257d)
- [SIP Cyber/Architecture Development and Demonstration Research Results](https://www8.cao.go.jp/cstp/stmain/a-1-1_200318.pdf)
