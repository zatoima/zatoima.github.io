---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Redshift RA3 と Spectrumの使い分け"
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








どちらもコンピュートとストレージ層が分離されているアーキテクチャのため、どういうユースケースのときにどっちを使うべきかという疑問。

- 例
  
  - RA3パターン
    - S3にデータをオフロードしてストレージを節約しているパターン等はRA3に
    - Redshift内でETLを行いデータを加工するパターン
    - S3上でのパーティション分割などSpectrumからのスキャン性能とかあまり気にしたくない時に
  - Spectrum
    - 他のAWSサービスからS3上のデータにアクセスするパターン。現時点においてもDWH上にデータを置いていないパターン等はSpectrumへ。（この場合はAthenaとの使い分けがまた悩みどころ…。）
    
    - EMRでデータを加工してRedshiftでデータを参照するパターン
    
    - Redshift内のデータと組み合わせて使うパターン
    
      <iframe src="//www.slideshare.net/slideshow/embed_code/key/zzxb6aeXSKNjwR?startSlide=69" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/AmazonWebServicesJapan/20200318-aws-black-belt-online-seminar-amazon-redshift" title="20200318 AWS Black Belt Online Seminar Amazon Redshift" target="_blank">20200318 AWS Black Belt Online Seminar Amazon Redshift</a> </strong> from <strong><a href="//www.slideshare.net/AmazonWebServicesJapan" target="_blank">Amazon Web Services Japan</a></strong> </div>

