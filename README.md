# j.money.api
A Rest API to manage personal finances.

### Project Setup
#### Build with Docker
- After cloning the project, access the folder on your terminal and run: `docker-compose build`;
- Then start the container by simply running: `docker-compose up`;
- To access the API endpoints, insert the following URL in your browser: `http://localhost:5065/`.
#### Sync the database
- Enter the container bash: `docker exec -it jmoney_api bash`;
- Run `flask db migrate -m "initial migration"` command;
- Run `flask db upgrade` command.


### Running Tests
- Enter the container bash: `docker exec -it jmoney_api bash`;
- Run `pytest` command.
