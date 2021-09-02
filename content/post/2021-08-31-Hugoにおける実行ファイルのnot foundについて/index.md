---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Hugoにおける実行ファイルのnot foundについて"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-about-executable-not-found in Hugo
date: 2021-08-31
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

## エラー

環境変数内にgoの実行ファイルが見つからないというエラーが発生する

```
D:\hugo\zatoima.github.io>hugo server
Error: failed to download modules: exec: "go": executable file not found in %PATH%
```

## 解決策

[公式ドキュメント](https://wowchemy.com/docs/guide/troubleshooting/#error-go-executable-not-found)に記載があった。

> ##### Error: Go executable not found
>
> [Install Hugo’s Go dependency](https://wowchemy.com/docs/getting-started/install-hugo-extended/). If you believe that Go is already installed, perhaps Hugo was unable to detect Go due to installing either Go or Hugo in an isolated way such as via Linux Snaps. Users on all major platforms have reported success installing Hugo and Go by following the [official Wowchemy installation guide](https://wowchemy.com/docs/getting-started/install-hugo-extended/). You can also browse or report issues with Hugo detecting Go on the [Hugo Forum](https://discourse.gohugo.io/).

Windowsの場合は、[こちらの公式ドキュメント](https://wowchemy.com/docs/getting-started/install-hugo-extended/)に記載のPowerShellを実行することでエラーが解消した

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iwr -useb get.scoop.sh | iex
```

```
scoop install git go hugo-extended
```

### 実行ログ

```
PS C:\Users\imaza> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iwr -useb get.scoop.sh | iex
Initializing...
Downloading scoop...
Extracting...
Creating shim...
Downloading main bucket...
Extracting...
Adding ~\scoop\shims to your path.
'lastupdate' has been set to '2021-08-23T20:01:11.4676027+09:00'
Scoop was installed successfully!
Type 'scoop help' for instructions.
PS C:\Users\imaza> scoop install git go hugo-extended
Installing '7zip' (19.00) [64bit]
7z1900-x64.msi (1.7 MB) [=====================================================================================] 100%
Checking hash of 7z1900-x64.msi ... ok.
Extracting 7z1900-x64.msi ... done.
Linking ~\scoop\apps\7zip\current => ~\scoop\apps\7zip\19.00
Creating shim for '7z'.
Creating shortcut for 7-Zip (7zFM.exe)
'7zip' (19.00) was installed successfully!
Installing 'git' (2.33.0.windows.1) [64bit]
PortableGit-2.33.0-64-bit.7z.exe (44.1 MB) [==================================================================] 100%
Checking hash of PortableGit-2.33.0-64-bit.7z.exe ... ok.
Extracting dl.7z ... done.
Linking ~\scoop\apps\git\current => ~\scoop\apps\git\2.33.0.windows.1
Creating shim for 'git'.
Creating shim for 'gitk'.
Creating shim for 'git-gui'.
Creating shim for 'tig'.
Creating shim for 'git-bash'.
Creating shortcut for Git Bash (git-bash.exe)
Creating shortcut for Git GUI (git-gui.exe)
'git' (2.33.0.windows.1) was installed successfully!
Installing 'go' (1.17) [64bit]
go1.17.windows-amd64.zip (143.4 MB) [=========================================================================] 100%
Checking hash of go1.17.windows-amd64.zip ... ok.
Extracting go1.17.windows-amd64.zip ... done.
Running installer script...
Linking ~\scoop\apps\go\current => ~\scoop\apps\go\1.17
Creating shim for 'go'.
Creating shim for 'gofmt'.
'go' (1.17) was installed successfully!
Notes
-----
Your GOROOT has been set to: C:\Users\imaza\scoop\apps\go\current
You can run 'go env GOROOT' to view this at any time.
"$env:USERPROFILE\go\bin" has been added to your PATH.
Installing 'hugo-extended' (0.87.0) [64bit]
hugo_extended_0.87.0_windows-64bit.zip (16.2 MB) [============================================================] 100%
Checking hash of hugo_extended_0.87.0_windows-64bit.zip ... ok.
Extracting hugo_extended_0.87.0_windows-64bit.zip ... done.
Linking ~\scoop\apps\hugo-extended\current => ~\scoop\apps\hugo-extended\0.87.0
Creating shim for 'hugo'.
'hugo-extended' (0.87.0) was installed successfully!
PS C:\Users\imaza>
```

