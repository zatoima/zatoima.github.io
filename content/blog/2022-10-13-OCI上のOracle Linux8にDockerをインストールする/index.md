---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OCI上のOracle Linux8にDockerをインストールする"
subtitle: ""
summary: " "
tags: ["OCI"]
categories: ["OCI"]
url: ici-oracle-linux-8-docker-install
date: 2022-10-13
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

### Docker

Docker20.10くらいからRHEL8系でもDockerが使えるようになったが、デフォのリポジトリ設定だとRedhatの`podman-docker`をインストールしようとしてくるのでどうにかDockerをメモ。

#### 環境設定

```
[opc@oci-arm ~]$ cat /etc/redhat-release
Red Hat Enterprise Linux release 8.6 (Ootpa)
[opc@oci-arm ~]$ cat /etc/oracle-release
Oracle Linux Server release 8.6
[opc@oci-arm ~]$ cat /etc/os-release
NAME="Oracle Linux Server"
VERSION="8.6"
ID="ol"
ID_LIKE="fedora"
VARIANT="Server"
VARIANT_ID="server"
VERSION_ID="8.6"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Oracle Linux Server 8.6"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:oracle:linux:8:6:server"
HOME_URL="https://linux.oracle.com/"
BUG_REPORT_URL="https://bugzilla.oracle.com/"

ORACLE_BUGZILLA_PRODUCT="Oracle Linux 8"
ORACLE_BUGZILLA_PRODUCT_VERSION=8.6
ORACLE_SUPPORT_PRODUCT="Oracle Linux"
ORACLE_SUPPORT_PRODUCT_VERSION=8.6
```

#### レポジトリ設定

```
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

```
[opc@oci-arm ~]$ sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
Adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
```

#### インストール

```
sudo dnf install -y docker-ce docker-ce-cli containerd.io
```

```
[opc@oci-arm ~]$ sudo dnf install -y docker-ce docker-ce-cli containerd.io
Docker CE Stable - aarch64                                                                                                     431 kB/s |  26 kB     00:00
Dependencies resolved.

〜省略〜

Installed:
  container-selinux-2:2.188.0-1.module+el8.6.0+20721+d8d917a9.noarch                 containerd.io-1.6.8-3.1.el8.aarch64
  docker-ce-3:20.10.18-3.el8.aarch64                                                 docker-ce-cli-1:20.10.18-3.el8.aarch64
  docker-ce-rootless-extras-20.10.18-3.el8.aarch64                                   fuse-common-3.3.0-15.0.2.el8.aarch64
  fuse-overlayfs-1.9-1.module+el8.6.0+20721+d8d917a9.aarch64                         fuse3-3.3.0-15.0.2.el8.aarch64
  fuse3-libs-3.3.0-15.0.2.el8.aarch64                                                libcgroup-0.41-19.el8.aarch64
  libslirp-4.4.0-1.module+el8.6.0+20721+d8d917a9.aarch64                             slirp4netns-1.2.0-2.module+el8.6.0+20721+d8d917a9.aarch64

Complete
```

#### インストール後作業

```
sudo gpasswd -a $(whoami) docker
sudo chgrp docker /var/run/docker.sock
```

これを実施しないと権限エラーとなる。

> [opc@oci-arm cli-plugins]$ docker ps
> Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json": dial unix /var/run/docker.sock: connect: permission denied

#### バージョン確認

```
[opc@oci-arm ~]$ docker -v
Docker version 20.10.18, build b40c2f6
```

```
[opc@oci-arm ~]$ docker version
Client: Docker Engine - Community
 Version:           20.10.18
 API version:       1.41
 Go version:        go1.18.6
 Git commit:        b40c2f6
 Built:             Thu Sep  8 23:10:56 2022
 OS/Arch:           linux/arm64
 Context:           default
 Experimental:      true

Server: Docker Engine - Community
 Engine:
  Version:          20.10.18
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.18.6
  Git commit:       e42327a
  Built:            Thu Sep  8 23:09:25 2022
  OS/Arch:          linux/arm64
  Experimental:     false
 containerd:
  Version:          1.6.8
  GitCommit:        9cd3357b7fd7218e4aec3eae239db1f68a5a6ec6
 runc:
  Version:          1.1.4
  GitCommit:        v1.1.4-0-g5fd4c4d
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```

#### Dockerの起動

```
sudo systemctl start docker
```

#### Dockerの自動起動設定

```
sudo systemctl enable docker
```

### docker-compose

- [Docker Compose CLI プラグインのインストール — Docker\-docs\-ja 20\.10 ドキュメント](https://docs.docker.jp/compose/install/compose-plugin.html#compose-install-the-plugin-manually)

この環境はarmなのでaarch64のバイナリを取得しているが、intel系の場合はここを別に変える必要あり。

```
curl -SL https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-linux-aarch64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

```
pc@oci-arm cli-plugins]$ docker-compose -v
Docker Compose version v2.11.2
```









