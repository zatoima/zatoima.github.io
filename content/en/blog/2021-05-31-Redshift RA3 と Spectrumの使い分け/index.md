---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "When to Use Redshift RA3 vs Spectrum"
subtitle: ""
summary: " "
tags: ["AWS","Redshift"]
categories: ["AWS","Redshift"]
url: aws-redshift-ra3-spectrum.html
date: 2021-05-31
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



Both have architectures where the compute and storage layers are separated, raising the question of which to use for which use case.

- Examples

  - RA3 patterns:
    - When offloading data to S3 to save storage, use RA3
    - When performing ETL within Redshift to process data
    - When you don't want to worry about Spectrum scan performance such as partitioning on S3
  - Spectrum:
    - When accessing data on S3 from other AWS services. If data is not currently in DWH, use Spectrum. (In this case, deciding between Athena is also a consideration...)

    - When processing data with EMR and referencing data with Redshift

    - When combining with data within Redshift

      <iframe src="//www.slideshare.net/slideshow/embed_code/key/zzxb6aeXSKNjwR?startSlide=69" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/20200318-aws-black-belt-online-seminar-amazon-redshift" title="20200318 AWS Black Belt Online Seminar Amazon Redshift" target="_blank">20200318 AWS Black Belt Online Seminar Amazon Redshift</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>
