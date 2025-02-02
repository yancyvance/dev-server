## dev-server

This requires docker to be installed. You can initially download both the **Dockerfile** and **docker-compose.yml** files on your machine.

Create a folder **uploads** in the current directory where both files are residing.

Afterward, run the following commands:

`docker compose build`

`docker compose up`

This service automatically pushes any updates from this repository.


### Accessing Web Interface

The web service listens to port 5000. Using a web browser, access it using:

`http://localhost:5000`
