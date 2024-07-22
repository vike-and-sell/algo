# Algo

Team comprised of Larissa (Scrum Master), Haley, and Angus (Company Scrum Master)

## Local Setup

Follow these steps to get started with local development:

- Ensure that docker engine and docker-compose is installed.
- Run `docker-compose up --build`

### NOTE

- The above instructions are only for the first time build, every other time you can simply run `docker-compose up`
- Every time a change is made you will have to hit CTRL + C to stop the docker-compose and then re-run `docker-compose up` to have the changes take effect.
- This takes a long time to come up, give it time and test to see if it is up by `curl http://localhost:4500/`, you should get a response of "Hello World"


### URLS:
- to use local version, ensure elastic_client is intialized using `http://elasticsearch-master:9200` in app.py. Then use `curl http://localhost:4500/` as base url.
- to perform curl requests on the deployed version (running on cluster) please ensure elastic_client is intialized using `http://elasticsearch-master:9200` in app.py, and use `http://serber.ddns.net:32500/` as  base-url
