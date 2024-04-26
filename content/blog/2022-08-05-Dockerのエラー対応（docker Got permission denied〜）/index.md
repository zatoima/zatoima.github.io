---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Dockerのエラー対応（docker Got permission denied～）"
subtitle: ""
summary: " "
tags: ["Docker"]
categories: ["Docker"]
url: docker-error-permission-denied
date: 2022-08-06
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





### エラー内容

-----

```sh
[ec2-user@bastin ~]$ docker run -e MF_ID -e MF_PASS -e ALPHAVANTAGE_API_KEY -it public.ecr.aws/h3b4x6x6/mfstockupdater:1d0c9ea
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/create": dial unix /var/run/docker.sock: connect: permission denied.
See 'docker run --help'.
```

### 対応内容

-----

```sh
sudo gpasswd -a $(whoami) docker
sudo chgrp docker /var/run/docker.sock
sudo service docker restart
```

```sh
[ec2-user@bastin ~]$ sudo gpasswd -a $(whoami) docker
Adding user ec2-user to group docker
[ec2-user@bastin ~]$ sudo chgrp docker /var/run/docker.sock
[ec2-user@bastin ~]$ sudo service docker restart
Redirecting to /bin/systemctl restart docker.service
```

