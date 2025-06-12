# Simple QR Code Generator - Translated to German

Largely based on [this project from pjanczyk](https://github.com/pjanczyk/qr-code-generator), but with major changes and cleanup to get it to actually work.
Deployment locally via docker is now working and SVGs now dont throw an error. Minor changes in the UI too.

<img src="docs/screenshot.png" width="600"/>

_**web**_ is a web application written in Spring and Kotlin. It uses Thymeleaf for server-side rendering.
Both services are dockerized.

### UI Design

[Figma project](https://www.figma.com/file/m0zkjHTBtYOHYB327GsUou/QR_Code_Generator?node-id=0%3A1)

### How to Use

1. **Install Docker** if you haven't already.
2. **Clone the Repository and build the image** using the following commands:

```bash
git clone https://github.com/FlyingT/qr-code-generator-german.git
```
```bash
cd qr-code-generator-german
```
```bash
docker compose up --build -d
```
The Web-UI will be published on Port 3007, so go to http://[IP-of-Host]:3007 to access it

If you want to use a different port, use this:
```bash
HOST_PORT=YOUR-FAVORITE-PORT docker compose up --build -d
```

Ignore this, its just for reinstalling:
```bash
docker container stop qr-code-generator-german
docker container qr-code-generator-german
docker system prune
cd ..
rm -r  qr-code-generator-german
```
