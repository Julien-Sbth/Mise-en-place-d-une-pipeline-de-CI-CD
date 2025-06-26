# TP 1 – Docker

## Exécuter un serveur web (apache, nginx, …) dans un conteneur docker

A. Créer un fichier HTML  

Dans un terminal, créer un dossier et un fichier `index.html` :

```bash
mkdir site
echo "<h1>Bonjour depuis un volume Docker !</h1>" > site/index.html
```

B. Démarrer un conteneur avec un volume (`-v`)  

```bash
docker run --name web-volume -p 8081:80 -v ${PWD}/site/index.html:/usr/share/nginx/html/index.html nginx
```

**Explication** :  
- `${PWD}/site/index.html` : fichier HTML local.
- `/usr/share/nginx/html/index.html` : destination dans le conteneur Nginx.

**Le conteneur s’exécute au premier plan.** Pour libérer le terminal, fais `Ctrl + C`, puis :

```bash
docker start -a web-volume
```  
C. Vérification  

Accéder dans le navigateur à :  
[http://localhost:8081](http://localhost:8081)

Résultat attendu dans le navigateur :  
```
Bonjour depuis un volume Docker !
```

D. Supprimer le conteneur  

```bash
docker rm -f web-volume
```

E. Alternative avec `docker cp` (sans volume)  

Démarrer un conteneur Nginx :

```bash
docker run --name web-cp -p 8081:80 nginx
```

Copier le fichier dans le conteneur :

```bash
docker cp site/index.html web-cp:/usr/share/nginx/html/index.html
```

➡ Accéder à nouveau à : [http://localhost:8081](http://localhost:8081)

Remarques  

Inconvénient, il faut réutiliser docker cp pour chaque modifications d'un fichier.


## 6. Créer une image Docker personnalisée avec un Dockerfile

Étapes pour créer une image Docker Nginx avec un fichier HTML personnalisé

### Préparer le dossier de travail

```bash
mkdir C:\Users\Julien\tp-docker\nginx-dockerfile
cd C:\Users\Julien\tp-docker\nginx-dockerfile
```

### Créer le fichier `Dockerfile`

```Dockerfile
FROM nginx
COPY index.html /usr/share/nginx/html/index.html
```

### Builder l’image Docker

```bash
docker build -t mon-nginx-image .
```

Le résultat de cette commande :  
`[+] Building...` puis `Successfully tagged mon-nginx-image`.

### Lancer un conteneur à partir de l’image

```bash
docker run -p --name web-dockerfile -p 8082:80 mon-nginx-image
```

### Vérification

Accéder à :  
```
[http://localhost:8082](http://localhost:8082)
```

Résultat attendu :  
**Le contenu de `index.html`** s'affiche via Nginx.

Avantage d’une image Docker : permet d’embarquer l’application et tous ses fichiers dans une seule image facilement transférable et réutilisable.

### Conclusion

- **Volume** : idéal pour un développement rapide et interactif.  
- **Dockerfile** : recommandé pour la production, le CI/CD, et la traçabilité.  
- **docker cp** : utile ponctuellement mais à éviter pour un usage régulier.


## 7 – Utiliser une base de données dans un conteneur Docker

Voici les étapes complètes pour utiliser **MySQL 5.7** et **phpMyAdmin** dans Docker sous Windows/WSL2 ou PowerShell.

### Objectif

Lancer deux conteneurs :

- `mysql:5.7` pour la base de données  
- `phpmyadmin/phpmyadmin` pour l’interface graphique
---
### Créer un dossier propre

```powershell
mkdir C:\Users\Julien\tp-docker\mysql-phpmyadmin
cd C:\Users\Julien\tp-docker\mysql-phpmyadmin
```
---

### Lancer les conteneurs avec Docker CLI
```powershell
docker network create my-net

docker run -d --name mysql57 --network my-net `
  -e MYSQL_ROOT_PASSWORD=rootpassword `
  -e MYSQL_DATABASE=demo `
  -e MYSQL_USER=demo `
  -e MYSQL_PASSWORD=demopass `
  mysql:5.7

docker run -d --name phpmyadmin \
  --link mysql57:mysql \
  -p 8082:80 \
  phpmyadmin/phpmyadmin

```
L’option --network my-net utilisée dans docker run permet de connecter un conteneur à ce réseau personnalisé.

Ainsi, tous les conteneurs qui sont lancés avec --network my-net peuvent :

    Se résoudre mutuellement par leur nom (ex : mysql57)
    Échanger des données entre eux via ce réseau isolé
---

### Accéder à phpMyAdmin

Naviguer vers :  
[http://localhost:8082](http://localhost:8082)

Identifiants à utiliser :

- **Serveur** : `mysql57`  
- **Utilisateur** : `demo`  
- **Mot de passe** : `demopass`

---

### Ajouter une table et quelques enregistrements

Créer une table `utilisateur` avec les colonnes : `id`, `email`, `password`.

---

### Résumé des commandes utilisées

```bash
docker network create my-net

docker run -d --name mysql57 --network my-net \
  -e MYSQL_ROOT_PASSWORD=rootpassword \
  -e MYSQL_DATABASE=demo \
  -e MYSQL_USER=demo \
  -e MYSQL_PASSWORD=demopass \
  mysql:5.7

docker run -d --name phpmyadmin --network my-net \
  -e PMA_HOST=mysql57 \
  -p 8082:80 \
  phpmyadmin/phpmyadmin
```

## 8 MySQL + phpMyAdmin avec `docker-compose.yml`

Voici comment faire exactement la même chose (MySQL + phpMyAdmin) avec un fichier `docker-compose.yml`, ainsi qu'une réponse claire aux questions posées.
---

### Créer un dossier pour le projet

```bash
mkdir ~/tp-docker/mysql-compose
cd ~/tp-docker/mysql-compose
```
---

### Créer le fichier `docker-compose.yml`

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:5.7
    container_name: mysql57
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: demo
      MYSQL_USER: demo
      MYSQL_PASSWORD: demopass
    networks:
      - mynet

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: phpmyadmin
    restart: always
    ports:
      - "8082:80"
    environment:
      PMA_HOST: mysql
    networks:
      - mynet

networks:
  mynet:
```

---

### Lancer les services

```bash
docker-compose up -d
```

Cela télécharge les images si besoin, crée le réseau, et lance les conteneurs.

---

### Accéder à phpMyAdmin

Aller sur :  
[http://localhost:8082](http://localhost:8082)

Identifiants :

- **Serveur** : `mysql`  
- **Utilisateur** : `demo`  
- **Mot de passe** : `demopass`

---

### Réponses aux questions

#### a. Qu’apporte `docker-compose.yml` par rapport aux `docker run` ?

 **Lisibilité** : tous les services, options et variables sont définis en un seul fichier clair.  
 **Reproductibilité** : tu peux recréer facilement ton environnement avec une seule commande.  
 **Gestion automatique des réseaux** : plus besoin de créer le réseau manuellement.  
 **Facilité de versionnage** : ton infra est décrite dans un fichier versionnable (Git).  
 **Simplicité** : `docker-compose up` fait tout (création, liens entre services, etc.).  
---

#### b. Quel moyen permet de configurer la base MySQL au lancement ?

Les **variables d’environnement** dans `docker-compose.yml` :

```yaml
environment:
  MYSQL_ROOT_PASSWORD: rootpassword
  MYSQL_DATABASE: demo
  MYSQL_USER: demo
  MYSQL_PASSWORD: demopass
```

## 9 – Observation de l’isolation réseau avec Docker Compose

---

### Étape A – Créer 3 services (`web`, `app`, `db`) et 2 réseaux

#### Fichier `docker-compose.yml`

```yaml
services:
  web:
    image: praqma/network-multitool
    container_name: web
    networks:
      - frontend

  app:
    image: praqma/network-multitool
    container_name: app
    networks:
      - frontend
      - backend

  db:
    image: praqma/network-multitool
    container_name: db
    networks:
      - backend

networks:
  frontend:
  backend:
```

---

### Démarrer les conteneurs

```bash
docker compose up -d
```
---

### Vérification de l’isolation avec `ping` + `docker inspect`

#### Tester les connexions réseau

```bash
docker exec -it web sh
ping db
Résultat "Try Again"
ping app
Résultat : Connexion OK
exit
```

```bash
docker exec -it db sh
ping web
Résultat "Try Again"
ping app
Résultat : Connexion OK
exit
```

```bash
docker exec -it app sh
ping web
Résultat : Connexion OK
ping db
docker exec -it app sh
exit
```

Conclusion : sur web, db et app, app peut seulement ping, sur db, app peut seulement ping, sur app, les deux peuvent communiquer

#### Justification avec `docker inspect`

```bash
docker inspect web
```

Résultat de la commande :

```json
[
    {
        "Id": "d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d",
        "Created": "2025-06-04T07:33:58.316173443Z",
        "Path": "/bin/sh",
        "Args": [
            "/docker/entrypoint.sh",
            "/usr/sbin/nginx",
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 2894,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2025-06-04T07:33:58.664311307Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:97b15098bb72df10f7c4e177b9c0e2435ec459f16e79ab7ae2ed3f1eb0e79d19",
        "ResolvConfPath": "/var/lib/docker/containers/d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d/hostname",
        "HostsPath": "/var/lib/docker/containers/d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d/hosts",
        "LogPath": "/var/lib/docker/containers/d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d/d1f95c211752fa9760bc47d964eda1542ca2783f9b0b13662e5099450163732d-json.log",
        "Name": "/web",
        "RestartCount": 0,
        "Driver": "overlayfs",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "patate_frontend",
            "PortBindings": {},
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "ConsoleSize": [
                0,
                0
            ],
            "CapAdd": null,
            "CapDrop": null,
            "CgroupnsMode": "host",
            "Dns": null,
            "DnsOptions": null,
            "DnsSearch": null,
            "ExtraHosts": [],
            "GroupAdd": null,
            "IpcMode": "private",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": null,
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": null,
            "DeviceCgroupRules": null,
            "DeviceRequests": null,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": false,
            "PidsLimit": null,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0,
            "MaskedPaths": [
                "/proc/asound",
                "/proc/acpi",
                "/proc/kcore",
                "/proc/keys",
                "/proc/latency_stats",
                "/proc/timer_list",
                "/proc/timer_stats",
                "/proc/sched_debug",
                "/proc/scsi",
                "/sys/firmware",
                "/sys/devices/virtual/powercap"
            ],
            "ReadonlyPaths": [
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger"
            ]
        },
        "GraphDriver": {
            "Data": null,
            "Name": "overlayfs"
        },
        "Mounts": [],
        "Config": {
            "Hostname": "d1f95c211752",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": true,
            "AttachStderr": true,
            "ExposedPorts": {
                "11443/tcp": {},
                "1180/tcp": {},
                "443/tcp": {},
                "80/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "/usr/sbin/nginx",
                "-g",
                "daemon off;"
            ],
            "Image": "praqma/network-multitool",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": [
                "/bin/sh",
                "/docker/entrypoint.sh"
            ],
            "OnBuild": null,
            "Labels": {
                "com.docker.compose.config-hash": "fda5dac22c63f9194f0a75529a9b9a6f366e71253c50831a377a27c53797300e",
                "com.docker.compose.container-number": "1",
                "com.docker.compose.depends_on": "",
                "com.docker.compose.image": "sha256:97b15098bb72df10f7c4e177b9c0e2435ec459f16e79ab7ae2ed3f1eb0e79d19",
                "com.docker.compose.oneoff": "False",
                "com.docker.compose.project": "patate",
                "com.docker.compose.project.config_files": "C:\\Users\\Julien\\tp-docker\\Patate\\docker-compose.yml",
                "com.docker.compose.project.working_dir": "C:\\Users\\Julien\\tp-docker\\Patate",
                "com.docker.compose.service": "web",
                "com.docker.compose.version": "2.31.0"
            }
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "191e23aa04943d4bee6012d438ad0deee9e2ef7e41fd948e04ad8e94e49569f1",
            "SandboxKey": "/var/run/docker/netns/191e23aa0494",
            "Ports": {
                "11443/tcp": null,
                "1180/tcp": null,
                "443/tcp": null,
                "80/tcp": null
            },
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "",
            "Gateway": "",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "",
            "IPPrefixLen": 0,
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "patate_frontend": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "web",
                        "web"
                    ],
                    "MacAddress": "02:42:ac:14:00:02",
                    "DriverOpts": null,
                    "NetworkID": "d93c8b9344e0864f545cd63942d545f9c1a08ce95b073506c1a06564605a5052",
                    "EndpointID": "3020b07cdfdedd3f77b6a64c9ce6f96355d10025aec49bb1e2438528107a1b4d",
                    "Gateway": "172.20.0.1",
                    "IPAddress": "172.20.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DNSNames": [
                        "web",
                        "d1f95c211752"
                    ]
                }
            }
        }
    }
]
```

## TP 2 – Application Node.js + MySQL avec Docker

---
### Création d'un fichier `.env`

```env
PORT=3000
DATABASE_HOST=mysql
DATABASE_PORT=3306
DATABASE_USERNAME=root
DATABASE_PASSWORD=rootpassword
DATABASE_NAME=ma_super_db
```
---
### Fichier `Dockerfile`

```Dockerfile
FROM node:12-alpine3.9

WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY . .

CMD ["node", "src/index.js"]
```
## Installation des dépendances

Pour installer toutes les dépendances nécessaires au bon fonctionnement du projet, exécutez la commande suivante dans le terminal à la racine du projet :

```bash
npm install
```
---
### Fichier `docker-compose.yml`

```yaml
version: '3.9'

services:
  node:
    build: .
    container_name: ma_super_app
    ports:
      - "3000:3000"
    depends_on:
      - mysql
    env_file: .env

  mysql:
    image: mysql:5.7
    container_name: mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: ma_super_db
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```
---

### Lancer l'application et MySQL

```bash
docker-compose up --build
```
Cela va :

- Construire l’image Docker pour l’application Node.js
- Démarrer un conteneur MySQL avec une base préconfigurée
- Lier les deux services via un réseau Docker interne
- Exposer l’application sur le port 3000
```
```

# TP3 React Docker App

## Lancement en local (mode développement)

L'application sera disponible sur : [http://localhost:3000](http://localhost:3000)

---

## Construction et exécution avec Docker

### 1. Construire l'image Docker

```bash
docker build -t react-docker-app .
```
## Structure du `Dockerfile`


```Dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Exécuter le conteneur

```bash
docker run -d -p 8080:80 react-docker-app
```
L'application sera disponible sur : [http://localhost:8080](http://localhost:8080)
---