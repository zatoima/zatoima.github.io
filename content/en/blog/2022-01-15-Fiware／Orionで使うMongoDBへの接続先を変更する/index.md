---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Changing the MongoDB Connection Used by Fiware/Orion"
subtitle: ""
summary: " "
tags: ["Docker","Fiware"]
categories: ["Docker","Fiware"]
url: fireware-orion-mongodb-connection-change
date: 2022-01-15
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, Bott
---

The reference manual is here. I wonder why the official Fiware manual is hard to find on Google.

- Docker - FIWARE-Orion https://fiware-orion.letsfiware.jp/user/docker/

> ### 2A. When MongoDB is on localhost
>
> To do this, run this command.
>
> ```
>  sudo docker run -d --name orion1 -p 1026:1026 fiware/orion
> ```
>
> Verify everything is working.
>
> ```
>  curl localhost:1026/version
> ```
>
> ### 2B. When MongoDB is running in another Docker container
>
> If you want to run MongoDB in another container, you can start it as follows:
>
> ```
>  sudo docker run --name mongodb -d mongo:4.4
> ```
>
> Then run Orion with this command:
>
> ```
>  sudo docker run -d --name orion1 --link mongodb:mongodb -p 1026:1026 fiware/orion -dbhost mongodb
> ```
>
> Verify everything is working.
>
> ```
>  curl localhost:1026/version
> ```
>
> This method is functionally equivalent to what was described in section 1, but manually performs the steps rather than using a docker-compose file. Data will be lost as soon as the MongoDB container is disabled.
>
> ### 2C. When MongoDB is running on a different host
>
> To connect to a different MongoDB instance, run the following command **instead of** the previous command:
>
> ```
>  sudo docker run -d --name orion1 -p 1026:1026 fiware/orion -dbhost <MongoDB Host>
> ```
>
> Verify everything is working.
>
> ```
>  curl localhost:1026/version
> ```
